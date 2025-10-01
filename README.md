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
# 🚀 YouTube Telegram Notification Bot

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-blue.svg)](https://telegram.org/)
[![YouTube](https://img.shields.io/badge/YouTube-API-red.svg)](https://developers.google.com/youtube)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> 🎯 **Automatically notify your Telegram channels when your favorite YouTubers upload new videos!**

A powerful Python bot that monitors YouTube channels and instantly sends beautiful notifications to your Telegram groups/channels whenever new videos are uploaded.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔄 **Real-time Monitoring** | Continuously watches multiple YouTube channels for new uploads |
| 📢 **Instant Notifications** | Sends immediate alerts to Telegram when videos are published |
| 🖼️ **Rich Media** | Beautiful notifications with video thumbnails and clickable links |
| 👥 **Multi-Group Support** | Send notifications to multiple Telegram groups simultaneously |
| 🔐 **Admin Control** | Secure admin-only access for bot management |
| ⚙️ **Easy Configuration** | Simple setup using environment variables |
| 💾 **Persistent Storage** | Remembers your settings between restarts |
| 🚀 **Auto-Retry** | Smart retry mechanism for failed notifications |
| 🛡️ **Error Handling** | Robust error handling and graceful shutdown |
| 🔗 **Telegram Groups** | Direct links to specific Telegram groups for each channel |

---

## 🎬 What You'll Get

When a new video is uploaded, your bot will send notifications like this:

```
🔥 NEW UPLOAD WATCH NOW 🔥
═══════════════════════════
🎬 Amazing Video Title
📺 Channel Name
📅 2024-10-01 15:30 UTC
Join_MyTG #ChannelName
```

---

## 📋 Prerequisites

Before you start, make sure you have:

- 🐍 **Python 3.8+** installed on your system
- 🔑 **YouTube Data API v3 key** (free from Google Cloud Console)
- 🤖 **Telegram Bot Token** (free from @BotFather)
- 📱 **Telegram User ID** (your admin ID)

---

## 🚀 Quick Start Guide

### Step 1: 📥 Download the Bot

```bash
git clone https://github.com/ryuchi311/YouTube-Telegram-Notification-Bot.git
cd YouTube-Telegram-Notification-Bot
```

### Step 2: 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: ⚙️ Create Configuration File

Create a `.env` file in the project folder:

```env
YOUTUBE_API_KEY=your_youtube_api_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
CHECK_INTERVAL=300
ADMIN_USERS=your_telegram_user_id_here
```

### Step 4: 🏃‍♂️ Run the Bot

```bash
python YT-BOT.py
```

---

## 🗂️ Project Structure

```
YouTube-Telegram-Notification-Bot/
├── 🤖 YT-BOT.py                 # Main bot application
├── ⚙️ telegram_config.py        # Configuration manager
├── 📦 requirements.txt          # Python dependencies
├── 🔐 .env                      # Your secret configuration
└── 📁 Pydata/                   # Data storage folder
    ├── 💬 telegram_chats.json   # Your active chat list
    └── 📺 influencers.json      # YouTube channels to monitor
```

---

## 🤖 Bot Commands Guide

### 📢 Notification Management Commands

| Command | Icon | Description | Example |
|---------|------|-------------|---------|
| `/start_notify` | 🚀 | Welcome message and bot introduction | Just type the command |
| `/help_notify` | ❓ | Show all available commands | Get complete help |
| `/how_notify` | 📖 | Step-by-step setup tutorial | Beginner's guide |
| `/add_telegram_notify` | ➕ | Add current chat to notification list | Use in your group |
| `/remove_notify` | ➖ | Remove current chat from notifications | Stop notifications here |
| `/list_notify` | 📝 | Show all chats receiving notifications | See your setup |
| `/pause_notify` | ⏸️ | Pause all YouTube notifications temporarily | Stop without removing config |
| `/unpause_notify` | ▶️ | Resume YouTube notifications | Start notifications again |
| `/status_notify` | 📊 | Show current bot status and statistics | Check if paused/running |
| `/enable_thumbnails` | 🖼️ | Enable thumbnail images in notifications | Show video previews |
| `/disable_thumbnails` | 📝 | Disable thumbnails (text-only messages) | Faster delivery, less data |

### 📺 YouTube Channel Management Commands

| Command | Icon | Description | Example |
|---------|------|-------------|---------|
| `/add_youtube_channel` | 🎬 | Add a YouTube channel (without Telegram group) | `/add_youtube_channel PewDiePie UC-lHJZR3Gqxm24_Vd_AJ5Yw` |
| `/add_youtube_channel_with_group` | 🔗 | Add YouTube channel with Telegram group link | `/add_youtube_channel_with_group MikeTamago UCR3aArAyYGXwJegyRGZ7WTg https://t.me/tamagowarriors` |
| `/remove_youtube_channel` | 🗑️ | Remove a YouTube channel from monitoring | `/remove_youtube_channel UC-lHJZR3Gqxm24_Vd_AJ5Yw` |
| `/list_youtube_channels` | 📋 | Show all monitored YouTube channels | See your channel list |

---

## 🛠️ Complete Setup Tutorial

### 🔑 Getting Your API Keys

#### 1. YouTube API Key
1. 🌐 Go to [Google Cloud Console](https://console.cloud.google.com/)
2. 📁 Create a new project or select existing one
3. 🔧 Enable "YouTube Data API v3"
4. 🔑 Create credentials (API Key)
5. 📋 Copy your API key

#### 2. Telegram Bot Token
1. 📱 Open Telegram and search for `@BotFather`
2. 💬 Send `/newbot` command
3. 📝 Choose a name and username for your bot
4. 🔑 Copy the bot token provided

#### 3. Your Telegram User ID
1. 📱 Search for `@userinfobot` in Telegram
2. 💬 Send `/start` to get your user ID
3. 📋 Copy the number (this is your admin ID)

### 🎯 Setting Up Your First Channel

1. **Find YouTube Channel ID:**
   - 🌐 Go to the YouTube channel
   - 📋 Copy from URL: `youtube.com/channel/CHANNEL_ID_HERE`
   - Or use online tools to find channel ID

2. **Add to Bot:**
   ```
   /add_youtube_channel_with_group ChannelName CHANNEL_ID https://t.me/your_group
   ```

3. **Set Up Notifications:**
   - ➕ Add bot to your Telegram group
   - 👑 Make bot an administrator
   - 💬 Use `/add_telegram_notify` in the group

---

## 🔧 Advanced Configuration

### ⏱️ Customizing Check Interval

Change how often the bot checks for new videos:

```env
CHECK_INTERVAL=300  # 5 minutes (default)
CHECK_INTERVAL=600  # 10 minutes
CHECK_INTERVAL=60   # 1 minute (not recommended - API limits)
```

### 👥 Multiple Admins

Add multiple admin users:

```env
ADMIN_USERS=123456789,987654321,555666777
```

---

## 🚨 Troubleshooting

### Common Issues and Solutions

| Problem | Solution |
|---------|----------|
| 🚫 "Bot was blocked by user" | Remove the chat with `/remove_notify` |
| ❌ "Invalid API key" | Check your YouTube API key in `.env` file |
| 🔐 "Unauthorized" | Verify your Telegram bot token |
| 📡 "Network timeout" | Check your internet connection |
| 🚯 "Admin only" | Make sure your user ID is in `ADMIN_USERS` |

### 📊 Checking Bot Status

The bot provides detailed logs:

```
✅ Sent notification to chat 123456789
⚠️ Network error for chat 987654321, retrying...
❌ Chat 555666777 not accessible (will be removed)
```

---

## 🎨 Customization Tips

### 🎭 Customize Notification Messages

Edit the `caption` in `process_video()` function to change notification format:

```python
caption = (
    f"🔥<b>NEW UPLOAD WATCH NOW</b>🔥\n"
    f"═══════════════\n"
    f"🎬 <b><a href='https://youtube.com/watch?v={video_id}'>{title}</a></b>\n"
    f"📺 <b><a href='https://youtube.com/channel/{channel_id}?sub_confirmation=1'>{channel_title}</a></b>\n"
    f"📅 {formatted_date}\n"
    f"{join_link} #{channel_title.replace(' ', '')}"
)
```

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. 🍴 Fork the repository
2. 🌿 Create your feature branch: `git checkout -b feature/amazing-feature`
3. 💾 Commit your changes: `git commit -m 'Add amazing feature'`
4. 📤 Push to the branch: `git push origin feature/amazing-feature`
5. 🔄 Open a Pull Request

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- 🤖 [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Amazing Telegram Bot API wrapper
- 📺 [google-api-python-client](https://github.com/googleapis/google-api-python-client) - YouTube Data API client
- 💡 [python-dotenv](https://github.com/theskumar/python-dotenv) - Environment variable management

---

## 💬 Support

- 📚 **Documentation**: Check this README for detailed instructions
- 🐛 **Issues**: Open an issue on GitHub for bug reports
- 💡 **Feature Requests**: Suggest new features via GitHub issues
- 📱 **Community**: Join our Telegram group for discussions

---

<div align="center">

### 🌟 Star this project if you found it helpful! 🌟

**Made with ❤️ by developers, for developers**

</div>

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
```
pip install python-telegram-bot
```
google-api-python-client - For YouTube API interactions
```
pip install google-api-python-client
```
python-dotenv - For environment variable management
```
pip install python-dotenv
```
aiohttp - For async HTTP requests
```
pip install aiohttp
```
APScheduler - For scheduling tasks
```
pip install APScheduler
```
## Optional but Recommended:

betterlogging - For improved logging capabilities

colorama - For colored terminal output

You can install all dependencies at once using:
```
pip install python-telegram-bot google-api-python-client python-dotenv aiohttp APScheduler
```
## Credentials
Key Environment Variables Required (.env file):
```
YOUTUBE_API_KEY=your_youtube_api_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
CHECK_INTERVAL=300
ADMIN_USERS=user_id1,user_id2
```
## To get started:

- Create a YouTube API key from Google Cloud Console
- Create a Telegram bot via BotFather and get the token
- Identify admin user IDs from Telegram
- Set up the .env file with these credentials
