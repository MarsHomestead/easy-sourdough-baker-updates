# Printable (and tablet) recipe cards

This folder holds a reusable recipe-card template for Easy Sourdough Baker. A published copy uses it so a baker can print a card to keep beside them, and can also open the same card on a tablet in the kitchen.

- `recipe-card.html` — layout, colors, and type. On screen it is a large-text, high-contrast kitchen view (one section at a time, with tappable fold checkboxes). When printed, `@media print` restores the compact letter-page card.
- `make_card.py` — fills the template from a JSON recipe and writes HTML, plus a PDF if Chrome or Chromium is available (`make_card.py RECIPE.json OUT.pdf`). You can also run `hive card RECIPE.json OUT.pdf`.

## Personal recipes

Keep each baker's recipe as their own JSON, for example `~/hive-mind/recipes/<slug>.json`. After every adjustment they ask for (their oven, their flours, their tools), update that file, add a short `history` line with a `why`, and re-render the card.

Hive Mind updates may refresh this template, but they must never overwrite a baker's personal recipe files.

## Filling a card

Amounts are in grams only. Leave a field off (or empty) to hide it.

Do not put someone else's copyrighted recipe on a card. Link their video or blog in the credit line instead. A card may still hold the baker's own notes and a fold tracker.

See the commented example in `recipe-card.html` for the JSON shape (`title`, `subtitle`, `credit`, `batch`, `sections`, `aside`, `history`, `notes_title`, `notes_lines`, `footer`).
