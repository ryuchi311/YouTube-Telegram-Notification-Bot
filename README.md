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
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create and configure `.env` file:
```env
YOUTUBE_API_KEY=your_youtube_api_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
CHECK_INTERVAL=300  # Check interval in seconds (default: 300)
ADMIN_USERS=user_id1,user_id2  # Comma-separated Telegram user IDs
```

## Project Structure

```
YouTube-Telegram-Notification-Bot/
├── YT-BOT.py                 # Updated main bot file
├── telegram_config.py        # Configuration management
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
└── Pydata/                  # Data directory
    ├── telegram_chats.json   # Active chat configurations
    └── influencers.json     # YouTube channel information
```

## Commands

### Notification Management
- `/start_notify` - Start the bot
- `/help_notify` - Show help message
- `/how_notify` - Show setup guide
- `/add_telegram_notify` - Add current chat to notification list
- `/remove_notify` - Remove current chat from notification list
- `/list_notify` - List all chats receiving notifications

### YouTube Channel Management
- `/add_youtube_channel` - Add a YouTube channel to monitor
- `/remove_youtube_channel` - Remove a YouTube channel
- `/list_youtube_channels` - List all monitored channels

## Setup Guide

1. **Channel Configuration:**
   - Get YouTube channel IDs for channels you want to monitor
   - Use `/add_youtube_channel [channel_name] [channel_id]`
   - Example: `/add_youtube_channel PewDiePie UC-lHJZR3Gqxm24_Vd_AJ5Yw`

2. **Telegram Setup:**
   - Add bot to target groups/channels
   - Make bot an administrator
   - Use `/add_telegram_notify` in each chat
   - Verify with `/list_notify`

## Features in Detail

### YouTube Monitoring
- Regular checking of new uploads (default: every 5 minutes)
- Smart caching of channel data to minimize API usage
- Efficient batch processing of video notifications

### Telegram Integration
- Rich message formatting with HTML support
- Automatic thumbnail extraction and sharing
- Batch notification processing to avoid rate limits
- Automatic cleanup of invalid chats

### Error Handling
- Connection retry mechanism
- Graceful shutdown handling
- Invalid chat cleanup
- Comprehensive error logging

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Telegram Bot API wrapper
- [google-api-python-client](https://github.com/googleapis/google-api-python-client) - YouTube Data API client


## Core Dependencies:

python-telegram-bot - For Telegram bot functionality

`pip install python-telegram-bot`

google-api-python-client - For YouTube API interactions

`pip install google-api-python-client`

python-dotenv - For environment variable management

`pip install python-dotenv`

aiohttp - For async HTTP requests

`pip install aiohttp`

APScheduler - For scheduling tasks

`pip install APScheduler`

Optional but Recommended:

betterlogging - For improved logging capabilities
colorama - For colored terminal output

You can install all dependencies at once using:

`pip install python-telegram-bot google-api-python-client python-dotenv aiohttp APScheduler`

Key Environment Variables Required (.env file):

YOUTUBE_API_KEY=your_youtube_api_key

TELEGRAM_BOT_TOKEN=your_telegram_bot_token

CHECK_INTERVAL=300

ADMIN_USERS=user_id1,user_id2

To get started:

Create a YouTube API key from Google Cloud Console
Create a Telegram bot via BotFather and get the token
Identify admin user IDs from Telegram
Set up the .env file with these credentials
