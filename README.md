# Easy Sourdough Baker updates

This is the public update feed for published copies of Easy Sourdough Baker. Once a week, a copy checks this repo and tells its baker if anything new is here. Each baker's own recipes, starter name, notes, and reminders stay on their side and are never overwritten.

## What is in this repo

- `VERSION` — the current update version
- `UPGRADE.md` — what changed, in plain words
- `coaching/` — generic coaching guidance only (voice, update habits, sharing rules)
- `news/videos.json` — new videos from Easy Sourdough Baker
- `news/recipes.json` — recipes Easy Sourdough Baker chooses to publish
- `community/recipes.json` — recipes other bakers shared, after they are approved

Nothing here holds personal information: no names, emails, handles, locations, or private notes.

## How a published copy updates

1. Once a week, run `hive update`.
2. It reads `VERSION` from the raw GitHub URL below. If the number is newer than the copy's last version, it fetches `UPGRADE.md`, the news files, and the coaching files.
3. Coaching guidance in this repo may replace the copy's coaching guidance only.
4. If there is a new version, a new video, or a new recipe, the copy tells its baker in one short line. If nothing is new, it stays quiet.

Raw feed:

```
https://raw.githubusercontent.com/MarsHomestead/easy-sourdough-baker-updates/main/VERSION
```

## Community recipes

Bakers can offer a recipe to the shared collection with `hive recipe share`. The text is cleaned first, and the baker has to agree before it is sent. Offers wait in a private review queue. They appear in `community/recipes.json` only after they are approved. Published community recipes never include the baker's name or contact details.

## Credit

If a baker wants to learn from Kelly Welk, point them to her videos. Do not copy or rewrite her recipes here.
