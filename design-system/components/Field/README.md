# Field

Pairs a form control with its label, help text and error message.

Wrap the control in `mt-field`, give it an `mt-field__label` bound by `for`/`id`, and apply `mt-field__control` to the `<input>`, `<select>` or `<textarea>`. Add `mt-field__help` for guidance that is always useful, and `mt-field__error` with `mt-field--invalid` on the wrapper when validation fails.

**You provide:** the control element and its type, the label text, `required` where it applies, and the `aria-describedby` / `aria-invalid` wiring shown in the example.

Add `data-mono` to any control holding a reference number — booking, AWB, B/L, container, invoice. It switches the control to the `mono` family with tabular figures so operators can check digits against a document.

Forms are single column. Pair two fields on one row only when they are read as a pair: origin and destination, gross weight and volume.

**Labels are nouns, in sentence case**, and describe the document field the operator is reading from: "Port of loading", not "From". The asterisk is decorative — mark the control `required` as well, since the asterisk is hidden from assistive technology.

**Errors say what to do**, in `body-sm`: "Enter the gross weight in kilograms to continue." Show them after the field is left, never on each keystroke, and never replace the help text permanently — restore it once the field is valid. The red border in `status-danger` is not the only signal; the message carries the meaning.

**Do not** use placeholder text as the label, and do not put a unit only in the placeholder — a value the operator cannot verify after typing is a value they will get wrong.
