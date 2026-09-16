# DataTable

The register view for shipments, quotations, invoices and documents — the platform's primary surface.

Apply `mt-table` to a real `<table>` with `<caption>`, `<thead>` and `scope="col"` headers. Mark the identifier cell `mt-table__ref` and every numeric cell `mt-table__num`, on both the `<th>` and the `<td>`.

**You provide:** the data, the column set, sorting and pagination controls, and the caption naming what the rows are and what filters produced them.

**Column order is fixed:** reference first, then the operational description, then state, then figures, then dates. In RTL the reference stays first in reading order, which places it at the right edge — the stylesheet handles this through logical properties, so do not reorder the markup per locale.

`mt-table__ref` sets the `mono` family with tabular figures and prevents wrapping, so a reference number can be checked character by character against a document. `mt-table__num` aligns to the end edge in both directions, so digits line up.

Where a figure is not yet confirmed, write the state — "Pending", "Confirmed on booking" — in the cell. Never render `0`, `—` or an estimated number in place of a real one.

Row hover tints to `surface-sunken`. Freeze the header with `shadow-sm` once the body scrolls.

**Below 768px**, do not shrink the table: switch to a stacked list of KeyValue pairs per record, keeping the reference as the heading. A horizontally scrolling operational table is unusable on a phone.

**Do not** use a table for layout, and do not hide a column at narrow widths if it carries state or a figure the operator acts on.
