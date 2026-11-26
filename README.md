# Disk Space Auditor

[![CI](https://github.com/KellerAI/disk-space-auditor/actions/workflows/ci.yml/badge.svg)](https://github.com/KellerAI/disk-space-auditor/actions/workflows/ci.yml)

Reclaim disk space without deleting anything you didn't approve.

```text
You:   My disk is almost full. What can go?
Agent: Disk: 82 GB used of 100 GB (82 percent). 18 GB available.
       Largest: downloads 21 GB | project copies 17 GB | render scratch 9 GB | caches 6 GB
       Low risk (approve all?): render scratch older than 14 days, 6 GB
       Needs your call: 3 duplicate project copies, 11 GB (2 clean, 1 has unpushed commits, left alone)
       Never touched: credentials, browser profiles, this agent's own data
       Which item do you approve first?
```

Illustrative transcript, not a recorded run. A recorded demo replaces it before the first release.

Audits disk usage on the computer your agent runs on, finds the biggest folders and likely leftovers, and proposes cleanup ranked by risk. Deletes only items you approve one by one. Portable Agent Plugins 1.0 package for Hermes Agent and for OpenAI Codex and the ChatGPT desktop app: one `plugin.json` and 2 skills.

## Install

Install lines pin the release payload commit. It holds every file the plugin loads; the `v0.1.0` tag adds only this pin to the README and the changelog.

Hermes Agent:

```bash
hermes plugins install KellerAI/disk-space-auditor --ref 85ebaf0054bf3416a774c2d598d46a00d3101e21 --no-enable
hermes plugins enable disk-space-auditor
```

Portable packages stay disabled until you enable them, and enabling takes effect on your next session. Hermes namespaces portable skills by plugin. On Hermes 0.22 they load as `agent-plugin-disk-space-auditor-6da82390:get-started`, `agent-plugin-disk-space-auditor-6da82390:run-audit`.

OpenAI Codex:

```bash
codex plugin marketplace add KellerAI/disk-space-auditor --ref 85ebaf0054bf3416a774c2d598d46a00d3101e21
codex plugin add disk-space-auditor@kellerai-disk-space-auditor
```

`codex plugin add` enables the plugin when it installs it. `codex plugin remove disk-space-auditor@kellerai-disk-space-auditor` uninstalls it and keeps the marketplace. Skills load in Codex as `disk-space-auditor:get-started`, `disk-space-auditor:run-audit`. The ChatGPT desktop app reads the same `.agents/plugins/marketplace.json` format according to OpenAI's plugin documentation; it has not been tested separately here.

Tested on 2026-11-26 with Hermes Agent 0.22.0 and Codex 0.166.0: pinned install, `hermes plugins validate` and `doctor`, and the Codex marketplace listing. Skill loading and enable/disable were verified on the sibling plugin `weekly-bot-upgrade-reviewer`, which has the same package layout; they were not repeated here.

## Skills

| Skill | Use it when |
|---|---|
| `get-started` | You have just enabled the plugin. It asks for protected folders, a warning level and your approval preference, then runs a first read-only audit. |
| `run-audit` | The disk is filling up, or you want cleanup candidates ranked by risk with a reclaim total. |

## What it needs

- A terminal tool from the host. Without one the plugin can only advise.
- Read-only size commands first (for example `df` and `du`); a delete runs only after you approve that exact path.


## What it does not do

- It does not delete, move or change a file without your yes on that exact item.
- It does not touch credentials, browser profiles, the agent's own data folders, installed skill or plugin folders, or anything on your protected list.
- It does not look at other computers or cloud storage.

## Disclosure

- Runs size and listing commands through your host's terminal tool, and delete commands only after your approval. The plugin ships no scripts of its own.
- No network calls of its own and no telemetry. Reads file names, sizes and dates; it does not open file contents unless needed to classify an item.
- Model calls are your host's own; the plugin adds none.
- Skills only: no tools, hooks, MCP servers, scripts, compiled binaries, stored credentials or telemetry.

## Honest limits

- Sizes are a point-in-time read and change while other work runs.
- Only this computer is visible. Risk labels are judgement calls; unsure items are listed and asked about.
- A deletion guard that enforces approval outside the model is planned for v0.2 and is not part of this release. Until then, rely on your host's command approval settings.
- The approval rule is an instruction to the model, not an enforced lock. Your host's approval settings are what actually block an unapproved action.

## Roadmap

Planned for v0.2, not built: a native Hermes `pre_tool_call` guard that blocks delete commands on protected paths and any delete you have not approved, with a cheat/legit test corpus and published false-block numbers. v0.1 is skills only.

## Measured evaluation

No measured results yet. `evals/cases.md` lists the scenarios each release is scored on. Results, including failures, are published here per release.

## Development

```bash
python -m unittest discover -s tests -v
python scripts/check_plugin.py
```

Standard library only; no install needed. See `AGENTS.md`.

## License and credit

Apache-2.0. See `LICENSE` and `NOTICE`.

Built by KellerAI (https://kellerai.io). KellerAI on X: [@KellerAI_KAI](https://x.com/kellerai_kai) · Jonathan Bowe, Co-Founder & COO, on X: [@KellerAI_COO](https://x.com/KellerAI_COO) · LinkedIn: https://www.linkedin.com/in/jonathan-bowe-kellerai

KellerAI is not affiliated with or endorsed by Nous Research, xAI or OpenAI.
