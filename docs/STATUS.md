# Project Status

## Current Goal

Build a POE2 opportunity monitor that:

- watches selected YouTube channels
- filters candidates by code rules and title patterns
- runs deeper analysis only on demand
- sends formatted alerts to Telegram
- stays extensible for future Reddit ingestion

## Current Architecture

- `config/channels.json`
  starter YouTube channel set for the first rollout
- `config/rules.json`
  formalized title-based keep/exclude rules for profitable POE2 content
- `src/poe2_monitor/sources/youtube.py`
  YouTube Data API integration for channel resolution and recent video discovery
- `src/poe2_monitor/analysis.py`
  analysis layer with title prefilter and safe fallback behavior
- `src/poe2_monitor/telegram_bot.py`
  Telegram alert formatting and delivery
- `src/poe2_monitor/storage.py`
  SQLite storage for discovered content and analyses
- `src/poe2_monitor/cli.py`
  CLI entrypoints for DB init, channel listing, one-shot runs, and Telegram testing

## Confirmed Decisions

- primary local model target: `qwen3:14b` via Ollama on the Windows PC
- selection strategy: code filters first, model analysis only by request
- focus scope: profitable POE2 content only
- excluded scope: builds, leveling, bossing, generic news
- alert language: source language
- delivery target: Telegram private chat

## Verified So Far

- local project scaffold exists and compiles
- local `.env` is used for secrets
- SQLite DB initialization works
- Telegram test message works
- Git repository is connected to `origin`

## Known Gaps

- OpenAI path is no longer the intended long-term inference path
- local Ollama integration is not implemented yet
- transcript acquisition is still incomplete
- no admin UI yet beyond config files and CLI
- no Reddit ingestion yet

## Recommended Next Steps On The PC

1. Install and start Ollama on the Windows PC.
2. Pull `qwen3:14b`.
3. Open this repository in Codex on that machine.
4. Replace the OpenAI analysis path with Ollama calls.
5. Keep title filtering as the default prefilter.
6. Add on-demand analysis command for queued candidate videos.
7. Add transcript retrieval and chunked summarization flow.
