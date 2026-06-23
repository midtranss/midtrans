#!/usr/bin/env python3
import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_FILES = [ROOT / "index.html", ROOT / "contact-us" / "index.html"]
REQUIRED_VALUES = [
    "+97142714480/1",
    "+971552928560",
    "+963119067",
    "+963933383858",
    "+963944334338",
]


class StaticPageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stylesheets = []
        self.canonicals = []
        self.hreflang = []
        self.in_jsonld = False
        self.jsonld_blocks = []
        self._jsonld_chunks = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "link" and attrs.get("rel") == "stylesheet":
            self.stylesheets.append(attrs.get("href"))
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonicals.append(attrs.get("href"))
        if tag == "link" and attrs.get("rel") == "alternate":
            self.hreflang.append((attrs.get("hreflang"), attrs.get("href")))
        if tag == "script" and attrs.get("type") == "application/ld+json":
            self.in_jsonld = True
            self._jsonld_chunks = []

    def handle_data(self, data):
        if self.in_jsonld:
            self._jsonld_chunks.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self.in_jsonld:
            self.jsonld_blocks.append("".join(self._jsonld_chunks))
            self.in_jsonld = False


def assert_page(path):
    text = path.read_text(encoding="utf-8")
    parser = StaticPageParser()
    parser.feed(text)

    assert re.search(r"<h1>.+?</h1>", text, re.S), f"{path}: missing visible h1"
    assert parser.canonicals, f"{path}: missing canonical"
    assert parser.hreflang, f"{path}: missing hreflang alternates"
    assert parser.jsonld_blocks, f"{path}: missing JSON-LD"

    for href in parser.stylesheets:
        if href and not href.startswith(("http://", "https://")):
            target = ROOT / href.lstrip("/") if href.startswith("/") else path.parent / href
            assert target.resolve().exists(), f"{path}: missing stylesheet {href}"

    for block in parser.jsonld_blocks:
        parsed = json.loads(block)
        assert parsed.get("@context") == "https://schema.org", f"{path}: invalid schema context"
        assert parsed.get("@graph"), f"{path}: schema graph is empty"

    for expected in REQUIRED_VALUES:
        assert expected in text, f"{path}: missing required contact value {expected}"


def main():
    for html_file in HTML_FILES:
        assert_page(html_file)

    print("Static site checks passed.")


if __name__ == "__main__":
    main()
