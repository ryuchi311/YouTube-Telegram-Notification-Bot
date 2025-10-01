# YouTube Telegram Notification Bot

A Python bot that monitors YouTube channels and automatically sends notifications to Telegram groups/channels when new videos are uploaded.

## Features

- 🔄 Real-time monitoring of multiple YouTube channels
- 📢 Instant notifications in Telegram when new videos are uploaded
- 🎯 Clean and professional notification format with thumbnails
- 👥 Support for multiple Telegram groups/channels
- 🔐 Admin-only access control
- ⚙️ Easy configuration via environment variables
- 💾 Persistent storage of channels and chat configurations
- 🚀 Automatic retry mechanism for failed notifications
- 🛡️ Error handling and graceful shutdown

## Prerequisites

- Python 3.8+
- YouTube Data API v3 key
- Telegram Bot Token
- Required Python packages (see `requirements.txt`)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ryuchi311/YouTube-Telegram-Notification-Bot.git
cd YouTube-Telegram-Notification-Bot
# YouTube Telegram Notification Bot

A simple, reliable Python bot that watches YouTube channels and sends notifications to Telegram groups/channels when new videos are published.

## Highlights

- Real-time monitoring of multiple YouTube channels
- Notifications with optional thumbnails and clickable links
- Smart link preview when thumbnails are disabled (small preview below text)
- Per-channel Telegram group links (Join_MyTG)
- Admin-only management commands
- Simple configuration via `.env` and `Pydata/` JSON files

## Quick start

1. Clone the repo:

```bash
git clone https://github.com/ryuchi311/YouTube-Telegram-Notification-Bot.git
cd YouTube-Telegram-Notification-Bot
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy the environment template and edit it:

```bash
cp .env.template .env
# Edit .env and set YOUTUBE_API_KEY and TELEGRAM_BOT_TOKEN
```

4. Run the bot:

```bash
python YT-BOT.py
```

## Files you care about

- `YT-BOT.py` — main application
- `telegram_config.py` — configuration manager (reads/writes `Pydata/`)
- `requirements.txt` — Python dependencies
- `Pydata/telegram_chats.json` — saved Telegram chats
- `Pydata/influencers.json` — monitored YouTube channels

## Docker (optional)

A `Dockerfile`, `docker-compose.yml`, and `docker-manage.sh` are included for containerized deployment. See `DOCKER.md`.

## Environment variables (in `.env`)

- `YOUTUBE_API_KEY` — required
- `TELEGRAM_BOT_TOKEN` — required
- `CHECK_INTERVAL` — seconds between checks (default 300)
- `THUMBNAILS_ENABLED` — true/false
- `NOTIFICATIONS_ENABLED` — true/false
- `ADMIN_USERS` — comma-separated Telegram user IDs

## Quick command reference

- `/start_notify` — ping bot and show welcome
- `/help_notify` — show help and available commands
- `/how_notify` — beginner setup steps
- `/add_telegram_notify` — add current chat to notifications (bot must be admin)
- `/remove_notify` — remove current chat from notifications
- `/list_notify` — list chats receiving notifications
- `/pause_notify` — pause notifications
- `/unpause_notify` — resume notifications
- `/status_notify` — show bot status and stats
- `/enable_thumbnails` — enable thumbnails in notifications
- `/disable_thumbnails` — send text-only notifications
- `/set_link_preview` — configure link preview options (saved in settings.json)
- `/add_youtube_channel <name> <id>` — add channel (no tg link)
- `/add_youtube_channel_with_group <name> <id> <tg_link>` — add channel with Telegram link
- `/remove_youtube_channel <id>` — remove a channel
- `/list_youtube_channels` — show monitored channels

## Notification preview

When a new video is detected the bot sends:

**With thumbnails enabled (default):**
```
🔥 NEW UPLOAD WATCH NOW 🔥
═══════════════════════════
🎬 <Video title (clickable)>
📺 <Channel (clickable)>
📅 <Upload date UTC>
<Join_MyTG (clickable if provided)> #ChannelName
```
*Includes video thumbnail image*

**With thumbnails disabled:**
```
🔥 NEW UPLOAD WATCH NOW 🔥
═══════════════════════════
🎬 <Video title (clickable)>
📺 <Channel (clickable)>
📅 <Upload date UTC>
<Join_MyTG (clickable if provided)> #ChannelName
```
*Includes small link preview below text (using LinkPreviewOptions)*

## Troubleshooting

- If the bot doesn't respond: check `.env` values and run `python YT-BOT.py` to view logs
- If `Chat not found` errors appear: the bot may have been removed or blocked from the group
- Network issues: the bot retries on transient errors; verify server connectivity

## Contributing

Fork, create a branch, implement changes, open a pull request.

## License

MIT

For the full command list and step-by-step beginner guide see `Pydata/command.txt`.
