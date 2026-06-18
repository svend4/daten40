# Invoice {{invoice_id}}

**Issue date:** {{issue_date}}
**Currency:** {{currency}}

## Seller
{{seller.name}}

## Buyer
{{buyer.name}}

## Lines
{{#each lines}}
- {{description}} — {{amount}}
{{/each}}

## Totals
Net: {{totals.net}}
VAT: {{totals.vat}}
Gross: {{totals.gross}}