# Easy Sourdough Baker Hive Mind client

A small Python 3 script with no secrets. Published copies of Easy Sourdough Baker use it to share anonymous baking lessons (only after a yes) and to check this repo for updates (and apply them only after a yes).

## Install

```
mkdir -p ~/hive-mind
curl -fsSL https://raw.githubusercontent.com/MarsHomestead/easy-sourdough-baker-updates/main/client/hive -o ~/hive-mind/hive
chmod +x ~/hive-mind/hive
```

Use a database that belongs to this copy only:

```
HIVE_DB=~/hive-mind/sourdough-hive.db ~/hive-mind/hive status
```

If the script already lives in `~/hive-mind/`, it uses `~/hive-mind/sourdough-hive.db` by default.

## Everyday commands

- `hive weekly` — show a cleaned preview of this week's share; send nothing
- `hive weekly --yes` — send that preview only after the baker says yes
- `hive update` — check this feed; print anything newer; apply nothing
- `hive update --yes` — apply coaching guidance only (never a baker's own recipes, starter name, notes, or reminders). May also refresh this client file.
- `hive on` / `hive off` / `hive status` / `hive shared`
- `hive lesson add ...` / `hive feedback send ...` / `hive recipe share ...`

Only bot setup information moves through Hive Mind: tools, workflows, tips and recommendations you may want to add. No personal information, passwords, account details or private data is ever sent or received. An update never asks for personal information, logins or account access. If one ever did, the client skips it and tells the baker. Everything happens only after a yes.

`hive review`, `hive approve`, and `hive publish` are for the bot's creator. On a published copy they exit with a short message and change nothing.

No paid plans. This file carries no keys or tokens.
