#!/usr/bin/env python3
"""
Tests for the live-log auditor.

The auditor's job is to read exports whose shape nobody controls. The tests that matter most are
therefore the shape tests and the failure-to-recognise test: an auditor that silently scans
nothing and prints "clean" is worse than no auditor at all.
"""

import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import audit_logs  # noqa: E402


class Args:
    """Stands in for the parsed argparse namespace."""

    def __init__(self, role_field=None, text_field=None, role_value=None):
        self.role_field = role_field
        self.text_field = text_field
        self.role_value = role_value


VIOLATION_EN = "The rate is USD 4500 per 40HC and transit is about 22 days."
VIOLATION_AR = "السعر حوالي 3200 دولار للحاوية والمدة ٢٥ يوماً تقريباً."
CLEAN_EN = (
    "I don't give figures myself. Could you tell me the commodity, the approximate weight, "
    "and whether you need door delivery?"
)
CLEAN_AR = "لا أعطي أرقاماً من عندي. ما هي البضاعة، وما الوزن التقريبي؟"

failures = []


def check(name, condition, detail=""):
    if condition:
        print(f"  ok   {name}")
    else:
        print(f"  FAIL {name}  {detail}")
        failures.append(name)


def write(suffix, content):
    fh = tempfile.NamedTemporaryFile("w", suffix=suffix, delete=False, encoding="utf-8")
    fh.write(content)
    fh.close()
    return fh.name


# --------------------------------------------------------------------------------------
print("\n=== export shapes ===")

# 1. Flat JSONL, one message per line.
path = write(".jsonl", "\n".join(json.dumps(r, ensure_ascii=False) for r in [
    {"conversation_id": "c1", "role": "user", "content": "How much to Damascus?"},
    {"conversation_id": "c1", "role": "assistant", "content": VIOLATION_EN},
    {"conversation_id": "c2", "role": "assistant", "content": CLEAN_EN},
]))
msgs, skipped = audit_logs.to_messages(audit_logs.load(path, "auto"), Args())
check("jsonl: assistant messages extracted", len(msgs) == 2, f"got {len(msgs)}")
check("jsonl: user row skipped", skipped == 1, f"got {skipped}")
report = audit_logs.scan(msgs)
check("jsonl: one message blocked", len(report.blocked) == 1, f"got {len(report.blocked)}")
check("jsonl: conversation attributed", report.flagged_conversations == {"c1"},
      str(report.flagged_conversations))

# 2. Nested conversations, Anthropic-style content blocks.
path = write(".json", json.dumps({"conversations": [
    {"session_id": "s9", "messages": [
        {"role": "user", "content": [{"type": "text", "text": "سعر الشحن؟"}]},
        {"role": "assistant", "content": [{"type": "text", "text": VIOLATION_AR}]},
    ]},
]}, ensure_ascii=False))
msgs, _ = audit_logs.to_messages(audit_logs.load(path, "auto"), Args())
check("nested: message extracted", len(msgs) == 1, f"got {len(msgs)}")
check("nested: conversation id carried", msgs and msgs[0].conversation == "s9",
      msgs[0].conversation if msgs else "none")
check("nested: content blocks flattened", msgs and "3200" in msgs[0].text)
check("nested: arabic violation caught", len(audit_logs.scan(msgs).blocked) == 1)

# 3. CSV with non-standard field names.
path = write(".csv", "sid,sender,body\nc7,MIRA,\"Transit is 18 days door to door.\"\n")
msgs, _ = audit_logs.to_messages(audit_logs.load(path, "csv"), Args())
check("csv: role value 'MIRA' recognised", len(msgs) == 1, f"got {len(msgs)}")
check("csv: transit claim blocked", len(audit_logs.scan(msgs).blocked) == 1)

# The check above passes "csv" explicitly, and that is how a real bug survived it: --format
# defaults to "auto", so nobody running this tool passes the flag. In auto mode a CSV went to
# the JSON parser and died with "Expecting value: line 1 column 1" — a message that tells the
# reader nothing, about a file that was never JSON. CSV is what an export button usually
# produces, and the documented example passes no --format at all.
#
# So these exercise the DEFAULT path. A test that only covers the flag covers the case nobody
# hits.
msgs, _ = audit_logs.to_messages(audit_logs.load(path, "auto"), Args())
check("auto: a .csv file is read as csv", len(msgs) == 1, f"got {len(msgs)}")

# An export saved under a name that does not say csv — .log, .txt — still has to work.
mislabelled = write(".log", "sid,sender,body\nc8,mira,\"Rate is 950 USD.\"\n")
msgs, _ = audit_logs.to_messages(audit_logs.load(mislabelled, "auto"), Args())
check("auto: a mislabelled csv is still read", len(msgs) == 1, f"got {len(msgs)}")
check("auto: and its content is still scanned",
      len(audit_logs.scan(msgs).blocked) == 1)

# The fallback must not swallow a genuinely unreadable file into silence — a tool that reports
# zero findings on a file it could not parse is the dangerous outcome this module exists to
# avoid, which is why an unscannable input exits 2 rather than 0.
junk = write(".txt", "this is not a log at all\njust prose\n")
try:
    audit_logs.load(junk, "auto")
    check("auto: junk still raises", False, "no exception")
except Exception:
    check("auto: junk still raises", True)

# JSONL is unaffected by any of it.
jl = write(".jsonl", '{"role":"assistant","content":"We guarantee space."}\n')
msgs, _ = audit_logs.to_messages(audit_logs.load(jl, "auto"), Args())
check("auto: jsonl still works", len(msgs) == 1, f"got {len(msgs)}")

# 4. Explicit field overrides win over auto-detection.
path = write(".jsonl", json.dumps({"who": "bot-reply", "said": VIOLATION_EN}) + "\n")
msgs, _ = audit_logs.to_messages(audit_logs.load(path, "auto"),
                                 Args(role_field="who", text_field="said",
                                      role_value="bot-reply"))
check("overrides: honoured", len(msgs) == 1, f"got {len(msgs)}")

# --------------------------------------------------------------------------------------
print("\n=== the failure that must never look like success ===")

path = write(".jsonl", json.dumps({"who": "bot", "said": VIOLATION_EN}) + "\n")
msgs, _ = audit_logs.to_messages(audit_logs.load(path, "auto"), Args())
report = audit_logs.scan(msgs)
check("unrecognised fields scan nothing", report.scanned == 0, f"got {report.scanned}")
check("unrecognised fields report no false clean", not report.blocked)
# The printed report must say ERROR, and main() must exit non-zero. Both are asserted in the
# CLI test below — this case exists because a silent zero is the dangerous outcome.

# --------------------------------------------------------------------------------------
print("\n=== redaction ===")

leaky = "Rate USD 4500. Contact me at ali@example.com or +971552928560."
msgs = [audit_logs.Message(text=leaky, conversation="c1", role="assistant")]
report = audit_logs.scan(msgs)
joined = " ".join(f.excerpt for _, v in report.blocked for f in v.findings)
check("redaction: email masked", "ali@example.com" not in joined)
check("redaction: phone masked", "971552928560" not in joined)
check("redaction: figure preserved", "4500" in joined, joined[:80])

report = audit_logs.scan(msgs, no_redact=True)
joined = " ".join(f.excerpt for _, v in report.blocked for f in v.findings)
check("no-redact: opt-out works", "ali@example.com" in joined)

# --------------------------------------------------------------------------------------
print("\n=== clean input stays clean ===")

msgs = [
    audit_logs.Message(text=CLEAN_EN, conversation="c1", role="assistant"),
    audit_logs.Message(text=CLEAN_AR, conversation="c2", role="assistant", lang="ar"),
]
report = audit_logs.scan(msgs)
check("clean: nothing blocked", not report.blocked,
      str([f.rule for _, v in report.blocked for f in v.findings]))
check("clean: both counted as scanned", report.scanned == 2)

# --------------------------------------------------------------------------------------
print("\n=== exit codes ===")

import subprocess  # noqa: E402

CLI = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "audit_logs.py")


def run(path, *extra):
    return subprocess.run([sys.executable, CLI, path, *extra],
                          capture_output=True, text=True)

path = write(".jsonl", json.dumps({"role": "assistant", "content": VIOLATION_EN}) + "\n")
res = run(path)
check("exit 1 on violation", res.returncode == 1, f"got {res.returncode}")
check("violation reported in output", "WOULD BE BLOCKED" in res.stdout)

path = write(".jsonl", json.dumps({"role": "assistant", "content": CLEAN_EN}) + "\n")
res = run(path)
check("exit 0 when clean", res.returncode == 0, f"got {res.returncode}")
check("clean output refuses to overclaim", "not proof that MIRA is safe" in res.stdout)

path = write(".jsonl", json.dumps({"who": "bot", "said": VIOLATION_EN}) + "\n")
res = run(path)
check("exit 2 when nothing recognised", res.returncode == 2, f"got {res.returncode}")
check("unrecognised export says ERROR", "ERROR" in res.stdout)

res = run("/tmp/definitely-not-a-real-file-9482.jsonl")
check("exit 2 on unreadable input", res.returncode == 2, f"got {res.returncode}")

# --------------------------------------------------------------------------------------
print()
if failures:
    print(f"MIRA log-audit suite: {len(failures)} FAILED — {', '.join(failures)}")
    sys.exit(1)
print("MIRA log-audit suite: all checks passed")
