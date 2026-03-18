# Jekyll collections migration notes

Prototype migrated on 2026-03-18:
- `zh/drinks` articles -> `_zh_drinks/`
- `en/drinks` articles -> `_en_drinks/`
- section index pages kept at:
  - `zh/drinks/index.html`
  - `en/drinks/index.html`

## URL preservation rule
Each migrated article now has an explicit `permalink` so the generated output URL remains unchanged.

Examples:
- source moved from `zh/drinks/light-milk-tea-return.html` to `_zh_drinks/light-milk-tea-return.html`
- output URL remains `/zh/drinks/light-milk-tea-return.html`

## Metadata added for the prototype
Added or normalized where missing:
- `permalink`
- `collection_key`
- `section`
- `date`
- `updated`
- `featured`
- `index_title`
- `index_description`

## Index behavior
Both drinks index pages now:
- iterate over the relevant collection
- sort articles by `date` descending
- render featured cards from `featured: true`
- render the full list from the same collection

## Next-step rollout ideas
After validating this prototype, the same pattern can be extended to:
- `zh/tea` / `en/tea`
- `zh/history` / `en/history`
- `zh/science` / `en/science`
- `zh/teaware` / `en/teaware`

## Caution
This prototype preserves article URLs, but homepage and cross-section indexes are still partly hand-curated. A full migration would likely add reusable include templates and possibly homepage-level aggregation from multiple collections.
