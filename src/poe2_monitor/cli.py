from __future__ import annotations

import argparse
import asyncio

from poe2_monitor.config_loader import load_channels
from poe2_monitor.pipeline import Pipeline
from poe2_monitor.settings import load_settings
from poe2_monitor.storage import Storage
from poe2_monitor.telegram_bot import TelegramSender


def _cmd_init_db() -> None:
    settings = load_settings()
    storage = Storage(settings.database_path)
    storage.init_db()
    print(f"Initialized database at {settings.database_path}")


def _cmd_channels_list() -> None:
    for channel in load_channels():
        status = "enabled" if channel.enabled else "disabled"
        print(f"{channel.channel_id}\t{channel.source}\t{status}\tpriority={channel.priority}")


def _cmd_run_once() -> None:
    pipeline = Pipeline()
    asyncio.run(pipeline.run_once())
    print("Pipeline run completed.")


def _cmd_test_telegram() -> None:
    settings = load_settings()
    sender = TelegramSender(
        token=settings.telegram_bot_token,
        chat_id=settings.telegram_chat_id,
    )
    asyncio.run(sender.send_alert("POE2 monitor test message"))
    print("Telegram test message sent.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="POE2 opportunity monitor")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("init-db")

    channels_parser = subparsers.add_parser("channels")
    channels_subparsers = channels_parser.add_subparsers(dest="channels_command", required=True)
    channels_subparsers.add_parser("list")

    subparsers.add_parser("run-once")
    subparsers.add_parser("test-telegram")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "init-db":
        _cmd_init_db()
        return
    if args.command == "channels" and args.channels_command == "list":
        _cmd_channels_list()
        return
    if args.command == "run-once":
        _cmd_run_once()
        return
    if args.command == "test-telegram":
        _cmd_test_telegram()
        return

    parser.error("unsupported command")
