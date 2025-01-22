import os
import asyncio
import aiohttp
import signal
import sys
import platform
from datetime import datetime, timezone
from dotenv import load_dotenv
from googleapiclient.discovery import build
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
from io import BytesIO
from telegram_config import TelegramConfig  # Import from local telegram_config.py file
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
)
from telegram.constants import ParseMode


# Load environment variables
load_dotenv()

class YouTubeTelegramBot:
    def __init__(self):
        self.youtube = build('youtube', 'v3', developerKey=os.getenv('YOUTUBE_API_KEY'))
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.bot = Bot(token=self.bot_token)
        self.admin_users = [int(uid) for uid in str(os.getenv('ADMIN_USERS', '')).split(',') if uid]
        self.config = TelegramConfig()
        self.check_interval = int(os.getenv('CHECK_INTERVAL', '300'))
        self.running = False
        self.last_check = {}
        self.shutdown_event = asyncio.Event()
        self.channel_cache = {}

    def is_admin(self, user_id: int) -> bool:
        """Check if user is an admin"""
        return user_id in self.admin_users

    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start_notify command"""
        user_id = update.effective_user.id
        if not self.is_admin(user_id):
            await update.message.reply_text(
                "⛔️ Sorry, only admin users can use this bot.\n"
                "Contact the bot owner to get access.",
                parse_mode=ParseMode.HTML
            )
            return

        await update.message.reply_text(
            f"👋 Welcome to the YouTube Monitor Bot!\n\n"
            f"Available commands:\n"
            f"/help_notify - Show all commands and usage\n"
            f"/add_telegram_notify - Add current chat to notification list\n"
            f"/remove_notify - Remove current chat from notification list\n"
            f"/list_notify - List all chats receiving notifications\n\n"
            f"Add me to your groups/channels and use these commands there!",
            parse_mode=ParseMode.HTML
        )


    #------------------------------------------------------------------------------------#
    async def cmd_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help_notify command"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            await update.message.reply_text(
                "⛔️ Sorry, only admin users can use this bot.",
                parse_mode=ParseMode.HTML
            )
            return

        help_text = (
            "🤖 <b>YouTube Notification Bot Help</b>\n\n"
            "<b>Available Commands:</b>\n\n"
            "🔔 <b>Notification Commands:</b>\n"
            "/add_telegram_notify - Add current chat to notification list\n"
            "/remove_notify - Remove current chat from notification list\n"
            "/list_notify - List all chats receiving notifications\n\n"
            "📺 <b>YouTube Channel Commands:</b>\n"
            "/add_youtube_channel - Add a YouTube channel to monitor\n"
            "/remove_youtube_channel - Remove a YouTube channel\n"
            "/list_youtube_channels - List all monitored channels\n\n"
            "❓ <b>Other Commands:</b>\n"
            "/start_notify - Show welcome message\n"
            "/help_notify - Show this help message\n"
            "/how_notify - Show quick setup guide\n\n"
            "For detailed setup instructions, use /how_notify"
        )

        await update.message.reply_text(
            help_text,
            parse_mode=ParseMode.HTML
        )

    async def cmd_how(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /how_notify command"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            await update.message.reply_text(
                "⛔️ Sorry, only admin users can use this bot.",
                parse_mode=ParseMode.HTML
            )
            return

        setup_text = (
            "🚀 <b>Bot Setup Guide</b>\n\n"
            "<b>1. Setting Up Notifications:</b>\n"
            "• Add bot to your group/channel\n"
            "• Make bot an administrator\n"
            "• Use /add_telegram_notify in the chat\n"
            "• Verify with /list_notify\n\n"
            "<b>2. Adding YouTube Channels:</b>\n"
            "• Find the YouTube channel ID\n"
            "• Use: /add_youtube_channel [channel_name] [channel_id]\n"
            "• Example: /add_youtube_channel PewDiePie UC-lHJZR3Gqxm24_Vd_AJ5Yw\n"
            "• Verify with /list_youtube_channels\n\n"
            "<b>3. Bot Operation:</b>\n"
            "• Bot checks for new videos every 5 minutes\n"
            "• Notifications are sent automatically\n"
            "• Ensure bot remains as admin\n\n"
            "<b>4. Management:</b>\n"
            "• Remove channels: /remove_youtube_channel [channel_id]\n"
            "• Stop notifications: /remove_notify\n"
            "• List settings: /list_notify and /list_youtube_channels\n\n"
            "For command list, use /help_notify"
        )

        await update.message.reply_text(
            setup_text,
            parse_mode=ParseMode.HTML
        )
    #------------------------------------------------------------------------------------#

    async def cmd_add(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /add_telegram_notify command"""
        user_id = update.effective_user.id
        chat_id = update.effective_chat.id
        chat_type = update.effective_chat.type
        
        if not self.is_admin(user_id):
            await update.message.reply_text(
                "⛔️ Sorry, only admin users can use this command.",
                parse_mode=ParseMode.HTML
            )
            return

        try:
            chat = await self.bot.get_chat(chat_id)
            chat_title = chat.title or str(chat_id)
            
            if self.config.add_chat(chat_id, chat_title, chat_type):
                await update.message.reply_text(
                    f"✅ Successfully added chat to notification list!\n\n"
                    f"Chat: <b>{chat_title}</b>\n"
                    f"Type: {chat_type}\n"
                    f"ID: <code>{chat_id}</code>\n\n"
                    f"Check /list_notify to see all configured chats.",
                    parse_mode=ParseMode.HTML
                )
            else:
                await update.message.reply_text(
                    f"ℹ️ This chat is already receiving notifications.\n\n"
                    f"Chat: <b>{chat_title}</b>\n"
                    f"ID: <code>{chat_id}</code>",
                    parse_mode=ParseMode.HTML
                )
        except Exception as e:
            await update.message.reply_text(
                f"❌ Error adding chat: {str(e)}",
                parse_mode=ParseMode.HTML
            )

    async def cmd_remove(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /remove_notify command"""
        user_id = update.effective_user.id
        chat_id = update.effective_chat.id
        
        if not self.is_admin(user_id):
            await update.message.reply_text(
                "⛔️ Sorry, only admin users can use this command.",
                parse_mode=ParseMode.HTML
            )
            return

        try:
            chat = await self.bot.get_chat(chat_id)
            chat_title = chat.title or str(chat_id)
            
            if self.config.remove_chat(chat_id):
                await update.message.reply_text(
                    f"✅ Successfully removed chat from notification list!\n\n"
                    f"Chat: <b>{chat_title}</b>\n"
                    f"ID: <code>{chat_id}</code>\n\n"
                    f"Use /add_telegram_notify to start receiving notifications again.",
                    parse_mode=ParseMode.HTML
                )
            else:
                await update.message.reply_text(
                    f"ℹ️ This chat was not in the notification list.\n\n"
                    f"Chat: <b>{chat_title}</b>\n"
                    f"ID: <code>{chat_id}</code>\n\n"
                    f"Use /add_telegram_notify to start receiving notifications.",
                    parse_mode=ParseMode.HTML
                )
        except Exception as e:
            await update.message.reply_text(
                f"❌ Error removing chat: {str(e)}",
                parse_mode=ParseMode.HTML
            )


    async def cmd_list(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /list_notify command"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            await update.message.reply_text(
                "⛔️ Sorry, only admin users can use this command.",
                parse_mode=ParseMode.HTML
            )
            return

        try:
            chats = self.config.get_chats()
            
            if not chats:
                await update.message.reply_text(
                    "📝 No chats are currently receiving notifications.\n\n"
                    "Use /add_telegram_notify in a group/channel to add it to the list.",
                    parse_mode=ParseMode.HTML
                )
                return

            chat_list = []
            for chat in chats:
                chat_id = chat['id']
                try:
                    chat_info = await self.bot.get_chat(chat_id)
                    chat_title = chat_info.title or str(chat_id)
                    chat_type = chat_info.type
                    chat_list.append(
                        f"• <b>{chat_title}</b>\n"
                        f"  Type: {chat_type}\n"
                        f"  ID: <code>{chat_id}</code>\n"
                        f"  Added: {chat.get('added_at', 'Unknown')}"
                    )
                except Exception:
                    chat_list.append(
                        f"• ID: <code>{chat_id}</code>\n"
                        f"  Type: {chat.get('type', 'unknown')}\n"
                        f"  Added: {chat.get('added_at', 'Unknown')}\n"
                        f"  (Unable to get current chat info)"
                    )

            message = "📝 <b>Chats receiving notifications:</b>\n\n" + "\n\n".join(chat_list)
            
            if len(message) > 4096:
                chunks = [message[i:i+4096] for i in range(0, len(message), 4096)]
                for chunk in chunks:
                    await update.message.reply_text(
                        chunk,
                        parse_mode=ParseMode.HTML
                    )
            else:
                await update.message.reply_text(
                    message,
                    parse_mode=ParseMode.HTML
                )
            
        except Exception as e:
            await update.message.reply_text(
                f"❌ Error listing chats: {str(e)}",
                parse_mode=ParseMode.HTML
            )

    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle Telegram errors"""
        print(f'Telegram Error: {context.error}')

   #------------------------------------------------------------------------------------#
    async def cmd_add_youtube_channel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /add_youtube_channel command"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            await update.message.reply_text(
                "⛔️ Sorry, only admin users can use this command.",
                parse_mode=ParseMode.HTML
            )
            return
        
        # Check command arguments
        if not context.args or len(context.args) < 2:
            await update.message.reply_text(
                "❌ Usage: /add_youtube_channel <channel_name> <channel_id>\n\n"
                "Example: /add_youtube_channel PewDiePie UC-lHJZR3Gqxm24_Vd_AJ5Yw",
                parse_mode=ParseMode.HTML
            )
            return
        
        channel_name = context.args[0]
        channel_id = context.args[1]
        
        try:
            # Verify channel exists on YouTube before adding
            response = self.youtube.channels().list(
                part="snippet",
                id=channel_id
            ).execute()
            
            if not response.get('items'):
                await update.message.reply_text(
                    f"❌ Could not find YouTube channel with ID: {channel_id}\n"
                    f"Please verify the channel ID is correct.",
                    parse_mode=ParseMode.HTML
                )
                return
            
            # Get actual channel name from YouTube if available
            actual_name = response['items'][0]['snippet']['title']
            
            if self.config.add_youtube_channel(actual_name, channel_id):
                await update.message.reply_text(
                    f"✅ Successfully added YouTube channel!\n\n"
                    f"Channel: <b>{actual_name}</b>\n"
                    f"ID: <code>{channel_id}</code>",
                    parse_mode=ParseMode.HTML
                )
            else:
                await update.message.reply_text(
                    f"ℹ️ This channel is already in the monitoring list.\n\n"
                    f"Channel: <b>{actual_name}</b>\n"
                    f"ID: <code>{channel_id}</code>",
                    parse_mode=ParseMode.HTML
                )
        
        except Exception as e:
            await update.message.reply_text(
                f"❌ Error adding channel: {str(e)}",
                parse_mode=ParseMode.HTML
            )

    async def cmd_remove_youtube_channel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /remove_youtube_channel command"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            await update.message.reply_text(
                "⛔️ Sorry, only admin users can use this command.",
                parse_mode=ParseMode.HTML
            )
            return
        
        if not context.args:
            await update.message.reply_text(
                "❌ Usage: /remove_youtube_channel <channel_id>\n\n"
                "Use /list_youtube_channels to see all channel IDs",
                parse_mode=ParseMode.HTML
            )
            return
        
        channel_id = context.args[0]
        channel = self.config.get_youtube_channel(channel_id)
        
        if self.config.remove_youtube_channel(channel_id):
            await update.message.reply_text(
                f"✅ Successfully removed YouTube channel!\n\n"
                f"Channel: <b>{channel['name']}</b>\n"
                f"ID: <code>{channel_id}</code>",
                parse_mode=ParseMode.HTML
            )
        else:
            await update.message.reply_text(
                f"❌ Channel with ID <code>{channel_id}</code> not found in monitoring list.\n\n"
                f"Use /list_youtube_channels to see all monitored channels.",
                parse_mode=ParseMode.HTML
            )

    async def cmd_list_youtube_channels(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /list_youtube_channels command"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            await update.message.reply_text(
                "⛔️ Sorry, only admin users can use this command.",
                parse_mode=ParseMode.HTML
            )
            return
        
        channels = self.config.get_youtube_channels()
        
        if not channels:
            await update.message.reply_text(
                "📝 No YouTube channels are currently being monitored.\n\n"
                "Use /add_youtube_channel to add a channel.",
                parse_mode=ParseMode.HTML
            )
            return
        
        channel_list = []
        for channel in channels:
            channel_list.append(
                f"• <b>{channel['name']}</b>\n"
                f"  ID: <code>{channel['id']}</code>"
            )
        
        message = "📝 <b>Monitored YouTube Channels:</b>\n\n" + "\n\n".join(channel_list)
        
        await update.message.reply_text(
            message,
            parse_mode=ParseMode.HTML
        )
    #----------------------------------------------------------------------------------#

    async def get_channel_id(self, channel_data):
        """Get channel ID from channel data dictionary"""
        try:
            channel_id = channel_data['id'].strip()
            channel_name = channel_data['name']
            
            # Check cache first
            if channel_id in self.channel_cache:
                return self.channel_cache[channel_id]

            # Verify the channel ID exists
            response = self.youtube.channels().list(
                part="id,snippet",
                id=channel_id
            ).execute()

            if response.get('items'):
                self.channel_cache[channel_id] = channel_id
                print(f"Successfully verified channel: {channel_name} ({channel_id})")
                return channel_id
            
            print(f"Could not verify channel ID {channel_id} for {channel_name}")
            return None

        except Exception as e:
            print(f"Error verifying channel {channel_data.get('name', 'Unknown')}: {str(e)}")
            return None

    async def check_channel(self, session, channel_data):
        """Check a YouTube channel for new uploads"""
        try:
            channel_id = await self.get_channel_id(channel_data)
            if not channel_id:
                print(f"Skipping channel {channel_data['name']} - could not verify ID {channel_data['id']}")
                return

            # Get videos after last check
            last_check_time = self.last_check.get(channel_id, datetime.now(timezone.utc).replace(
                hour=0, minute=0, second=0, microsecond=0
            )).isoformat()

            activities = self.youtube.activities().list(
                part="contentDetails,snippet",
                channelId=channel_id,
                publishedAfter=last_check_time,
                maxResults=5
            ).execute()

            videos_to_process = []
            for item in activities.get('items', []):
                if 'upload' not in item.get('contentDetails', {}):
                    continue

                video_id = item['contentDetails']['upload']['videoId']
                video = self.youtube.videos().list(
                    part="snippet,statistics,contentDetails",
                    id=video_id
                ).execute()['items'][0]

                upload_date = datetime.fromisoformat(video['snippet']['publishedAt'].replace('Z', '+00:00'))
                videos_to_process.append((upload_date, video))

            # Sort videos by upload date, newest first
            videos_to_process.sort(key=lambda x: x[0], reverse=True)

            for upload_date, video in videos_to_process:
                await self.process_video(session, video)

            # Update last check time
            self.last_check[channel_id] = datetime.now(timezone.utc)

        except Exception as e:
            print(f"Error checking {channel_data['name']}: {str(e)}")
            await asyncio.sleep(5)

    async def process_video(self, session, video):
        """Process a single video and send notifications"""
        if self.shutdown_event.is_set():
            return

        video_id = video['id']
        thumbnail_url = (
            video['snippet']['thumbnails'].get('maxres') or 
            video['snippet']['thumbnails'].get('high') or 
            video['snippet']['thumbnails']['default']
        )['url']

        async with session.get(thumbnail_url) as response:
            if response.status != 200:
                return
            thumbnail_data = await response.read()

        duration = video['contentDetails']['duration'].replace('PT','').lower()
        duration = duration.replace('h', ':').replace('m', ':').replace('s', '')
        
        upload_date = datetime.fromisoformat(video['snippet']['publishedAt'].replace('Z', '+00:00'))
        formatted_date = upload_date.strftime('%Y-%m-%d %H:%M UTC')

        caption = (
            f"🔥<b>NEW UPLOAD WATCH NOW</b>🔥\n"
            f"═══════════════\n"
            f"🎬 <b><a href='https://youtube.com/watch?v={video_id}'>{video['snippet']['title']}</a></b>\n"
            f"📺 <b><a href='https://youtube.com/channel/{video['snippet']['channelId']}?sub_confirmation=1'>{video['snippet']['channelTitle']}</a></b>\n"
         #   f"⏰ {duration} ┊ 👁 {int(video['statistics'].get('viewCount', 0)):,}\n"
            f"📅 {formatted_date}\n"
         #   f"🎯 <b>WATCH HERE:</b>\n"
         #   f"https://youtube.com/watch?v={video_id}\n\n"
            f"#NewVideo #{video['snippet']['channelTitle'].replace(' ', '')}"
        )

        await self.send_notifications(thumbnail_data, caption)

    async def send_notifications(self, thumbnail_data, caption):
        """Send notifications to all configured Telegram chats"""
        chat_ids = self.config.get_telegram_chats()
        total_chats = len(chat_ids)
        
        batch_size = 3
        for i in range(0, total_chats, batch_size):
            if self.shutdown_event.is_set():
                return
                
            batch = chat_ids[i:i + batch_size]
            for chat_id in batch:
                await self.send_notification_to_chat(chat_id, thumbnail_data, caption)
            
            if i + batch_size < total_chats:
                await asyncio.sleep(3)

    async def send_notification_to_chat(self, chat_id, thumbnail_data, caption):
        """Send notification to a single chat"""
        try:
            await self.bot.send_photo(
                chat_id=chat_id,
                photo=BytesIO(thumbnail_data),
                caption=caption,
                parse_mode=ParseMode.HTML,
                read_timeout=30,
                write_timeout=30,
                connect_timeout=30,
                pool_timeout=30
            )
            print(f"✅ Sent notification to chat {chat_id}")
            await asyncio.sleep(2)
            
        except Exception as e:
            error_message = str(e).lower()
            if "chat not found" in error_message or "bot was blocked" in error_message:
                print(f"❌ Chat {chat_id} not accessible (will be removed): {str(e)}")
                self.config.remove_telegram_chat(chat_id)
                return
            
            if "timeout" in error_message or "connection" in error_message:
                print(f"⚠️ Network error for chat {chat_id}, retrying once: {str(e)}")
                await asyncio.sleep(5)
                try:
                    await self.bot.send_photo(
                        chat_id=chat_id,
                        photo=BytesIO(thumbnail_data),
                        caption=caption,
                        parse_mode=ParseMode.HTML,
                        read_timeout=30,
                        write_timeout=30,
                        connect_timeout=30,
                        pool_timeout=30
                    )
                    print(f"✅ Retry successful for chat {chat_id}")
                except Exception as retry_e:
                    print(f"❌ Retry failed for chat {chat_id}: {str(retry_e)}")
            else:
                print(f"❌ Failed to send to chat {chat_id}: {str(e)}")

    async def monitor_channels(self):
        """Main monitoring loop"""
        self.running = True
        while not self.shutdown_event.is_set():
            try:
                channels = self.config.get_youtube_channels()
                print(f"\nChecking {len(channels)} channels at {datetime.now()}")
                print("Channels to check:", ", ".join(c['name'] for c in channels))

                conn = aiohttp.TCPConnector(limit=5, force_close=True)
                timeout = aiohttp.ClientTimeout(total=60)
                
                async with aiohttp.ClientSession(connector=conn, timeout=timeout) as session:
                    tasks = []
                    for channel_data in channels:
                        if self.shutdown_event.is_set():
                            break
                        task = asyncio.create_task(self.check_channel(session, channel_data))
                        tasks.append(task)
                        await asyncio.sleep(2)
                    
                    if tasks:
                        await asyncio.gather(*tasks, return_exceptions=True)

                if self.shutdown_event.is_set():
                    break

                print("\nWaiting for next check...")
                try:
                    await asyncio.wait_for(
                        self.shutdown_event.wait(), 
                        timeout=self.check_interval
                    )
                except asyncio.TimeoutError:
                    pass

            except Exception as e:
                print(f"Monitor error: {str(e)}")
                await asyncio.sleep(30)

        print("Monitor stopped cleanly")
        self.running = False

    async def run(self):
        """Run both the monitor and Telegram bot"""
        application = Application.builder().token(self.bot_token).build()
        
        # Add command handlers
        application.add_handler(CommandHandler('start_notify', self.cmd_start))
        application.add_handler(CommandHandler('help_notify', self.cmd_help))
        application.add_handler(CommandHandler('how_notify', self.cmd_how))
        application.add_handler(CommandHandler('add_telegram_notify', self.cmd_add))
        application.add_handler(CommandHandler('remove_notify', self.cmd_remove))
        application.add_handler(CommandHandler('list_notify', self.cmd_list))
        
        # YouTube channel management commands
        application.add_handler(CommandHandler('add_youtube_channel', self.cmd_add_youtube_channel))
        application.add_handler(CommandHandler('remove_youtube_channel', self.cmd_remove_youtube_channel))
        application.add_handler(CommandHandler('list_youtube_channels', self.cmd_list_youtube_channels))
        
        application.add_error_handler(self.error_handler)

        # Start application and monitoring
        async with application:
            await application.initialize()
            await application.start()
            await application.updater.start_polling()

            monitor_task = asyncio.create_task(self.monitor_channels())

            # Set up signal handlers
            if platform.system() != 'Windows':
                loop = asyncio.get_running_loop()
                for sig in (signal.SIGTERM, signal.SIGINT):
                    loop.add_signal_handler(
                        sig,
                        lambda s=sig: asyncio.create_task(self.handle_shutdown(application, monitor_task, s))
                    )
            else:
                for sig in (signal.SIGTERM, signal.SIGINT):
                    signal.signal(
                        sig,
                        lambda s, f, app=application, task=monitor_task: 
                            asyncio.create_task(self.handle_shutdown(app, task, s))
                    )

            try:
                await monitor_task
            except asyncio.CancelledError:
                pass

    async def handle_shutdown(self, application, monitor_task, sig):
        """Handle shutdown signal"""
        print(f"\nReceived signal {sig}")
        self.shutdown_event.set()
        monitor_task.cancel()
        await application.stop()
        await application.shutdown()
        sys.exit(0)

async def main():
    bot = YouTubeTelegramBot()
    bot.config.list_all()
    await bot.run()

if __name__ == "__main__":
    print("Starting YouTube Monitor and Telegram Bot...")
    asyncio.run(main())