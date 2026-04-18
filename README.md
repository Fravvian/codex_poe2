# POE2 Opportunity Monitor

POE2 Opportunity Monitor tracks selected YouTube channels, analyzes new videos,
filters for profitable opportunities, and sends instant Telegram alerts.

The initial architecture is intentionally source-agnostic so Reddit ingestion
can be added later without rewriting the core pipeline.

## What V1 Includes

- YouTube source registry with an initial starter set of channels
- Analysis pipeline interfaces for metadata, transcripts, filtering, and alerts
- Profit-focused rules config
- SQLite storage layer
- Telegram alert formatter and sender
- Simple CLI admin workflow for listing and toggling channels

## Planned Alert Shape

```text
Тип: фарм / торговля / абуз / крафт
Механика: ritual / breach / maps / temple / market / exploit / etc
Содержание: кратко, в чем идея и почему она приносит прибыль
To-do: что именно нужно сделать в игре
Требования: что нужно для запуска схемы
Риски: от чего зависит профит, что может сломать схему
Источник: ссылка на видео
```

Alerts should be sent in the source language whenever the analysis is confident
enough to classify the material as profit-focused POE2 content.

## Quick Start

1. Create and activate a virtual environment.
2. Install the package:

   ```bash
   pip install -e .
   ```

3. Copy `.env.example` to `.env` and fill in secrets.
4. Initialize the local database:

   ```bash
   poe2-monitor init-db
   ```

5. List configured channels:

   ```bash
   poe2-monitor channels list
   ```

6. Run one pipeline cycle:

   ```bash
   poe2-monitor run-once
   ```

## Notes

- The Telegram bot token should be rotated before production use because the
  current token has already been exposed during setup.
- The current codebase provides a solid scaffold and storage model, but the
  external provider integrations still need live API wiring and prompt tuning.
