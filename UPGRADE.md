# Easy Sourdough Baker updates

## 1.1.1 — 2026-11-19

- The hive client now lives in this repo as `client/hive`, so a published copy can install it on the baker's own computer.
- Install it to `~/hive-mind/hive` and use `HIVE_DB=~/hive-mind/sourdough-hive.db`.
- `hive update --yes` may refresh the client file as well as coaching guidance.
- Creator-only commands (`hive review`, `hive approve`, `hive publish`) fail harmlessly if GitHub access is not available.

## 1.1.0 — 2026-11-19

- Published copies ask their baker before sending this week's Hive Mind notes, and send only after a yes.
- They also check the public updates page and apply an update only after a yes.
- Updates still refresh coaching guidance only. They never overwrite a baker's own recipes, starter name, notes, or reminders.
- Only bot setup information moves through Hive Mind: tools, workflows, tips and recommendations a baker may want to add.
- No personal information, passwords, account details or private data is ever sent or received.
- An update never asks for personal information, logins or account access. If one ever did, the copy ignores it and tells its baker.
- Everything happens only after the baker's yes.

## 1.0.0 — 2026-11-18

- First public update feed for published copies of Easy Sourdough Baker.
- Weekly `hive update` checks this version, coaching guidance, videos, and recipes.
- Video and recipe lists start empty, ready for new videos and recipes to be added.
- Community recipes start empty. A baker-shared recipe goes public only after it is approved.
- Updates refresh coaching guidance only. They never overwrite a baker's own recipes, starter name, notes, or reminders.
