import json
import os
from datetime import datetime
from pathlib import Path

class TelegramConfig:
    def __init__(self):
        # Set the data folder relative to the current working directory
        self.data_folder = Path('pydata')
        self.chats_file = self.data_folder / 'telegram_chats.json'
        self.channels_file = self.data_folder / 'influencers.json'  # Note the 's' here
        self.ensure_data_folder()
        self.load_chats()
        self.load_channels()

    def ensure_data_folder(self):
        """Create pydata folder and initialize files if they don't exist"""
        # Create pydata folder
        if not self.data_folder.exists():
            print(f"Creating data folder: {self.data_folder}")
            self.data_folder.mkdir(parents=True)

        # Initialize telegram_chats.json if doesn't exist
        if not self.chats_file.exists():
            print(f"Initializing chats file: {self.chats_file}")
            self.save_chats([])

        # Initialize influencers.json if doesn't exist
        if not self.channels_file.exists():
            print(f"Initializing channels file: {self.channels_file}")
            initial_channels = {
                "channels": [
                    {"name": "MikeTamago-", "id": "UCR3aArAyYGXwJegyRGZ7WTg"},
                    {"name": "ALROCK", "id": "UC-sXVjY3Lw1IGxsme-_4ixA"},
                    {"name": "Dongayantv", "id": "UCG0y34BqW7ERseyMEsIJaOA"},
                ]
            }
            with open(self.channels_file, 'w') as f:
                json.dump(initial_channels, f, indent=4)

    def load_chats(self):
        """Load chats from JSON file"""
        try:
            with open(self.chats_file, 'r') as f:
                self.chats = json.load(f)
            print(f"Loaded {len(self.chats)} chats from {self.chats_file}")
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"No existing chats file found, starting fresh")
            self.chats = []
            self.save_chats(self.chats)

    def load_channels(self):
        """Load YouTube channels from influencers.json"""
        try:
            with open(self.channels_file, 'r') as f:
                data = json.load(f)
                self.channels = data.get('channels', [])
            print(f"Loaded {len(self.channels)} channels from {self.channels_file}")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading channels file: {str(e)}")
            self.channels = []

    def save_chats(self, chats):
        """Save chats to JSON file"""
        with open(self.chats_file, 'w') as f:
            json.dump(chats, f, indent=2)
        self.chats = chats
        print(f"Saved {len(chats)} chats to {self.chats_file}")

    def add_chat(self, chat_id: int, chat_title: str = None, chat_type: str = None) -> bool:
        """Add a chat to the list if not already present"""
        chat_id = int(chat_id)  # Ensure chat_id is int
        
        # Check if chat already exists
        if chat_id in [chat['id'] for chat in self.chats]:
            print(f"Chat {chat_id} already exists in config")
            return False
        
        # Add new chat with metadata
        chat_data = {
            'id': chat_id,
            'title': chat_title or str(chat_id),
            'type': chat_type or 'unknown',
            'added_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        self.chats.append(chat_data)
        self.save_chats(self.chats)
        print(f"Added new chat: {chat_data}")
        return True

    def remove_chat(self, chat_id: int) -> bool:
        """Remove a chat from the list"""
        chat_id = int(chat_id)  # Ensure chat_id is int
        original_length = len(self.chats)
        
        # Remove chat if exists
        self.chats = [chat for chat in self.chats if chat['id'] != chat_id]
        
        if len(self.chats) < original_length:
            self.save_chats(self.chats)
            print(f"Removed chat {chat_id}")
            return True
        print(f"Chat {chat_id} not found in config")
        return False

    #-------------------------------------------------------------------------#
    def add_youtube_channel(self, channel_name: str, channel_id: str) -> bool:
        """Add a new YouTube channel to the configuration"""
        # Clean the input
        channel_name = channel_name.strip()
        channel_id = channel_id.strip()
        
        # Check if channel already exists
        if any(c['id'] == channel_id for c in self.channels):
            return False
            
        # Add new channel
        self.channels.append({
            'name': channel_name,
            'id': channel_id
        })
        
        # Save to file
        with open(self.channels_file, 'w') as f:
            json.dump({'channels': self.channels}, f, indent=4)
        
        return True

    def remove_youtube_channel(self, channel_id: str) -> bool:
        """Remove a YouTube channel from the configuration"""
        channel_id = channel_id.strip()
        original_length = len(self.channels)
        
        # Remove channel if exists
        self.channels = [c for c in self.channels if c['id'] != channel_id]
        
        if len(self.channels) < original_length:
            # Save updated list to file
            with open(self.channels_file, 'w') as f:
                json.dump({'channels': self.channels}, f, indent=4)
            return True
        
        return False

    def get_youtube_channel(self, channel_id: str) -> dict:
        """Get a specific YouTube channel's information"""
        channel_id = channel_id.strip()
        for channel in self.channels:
            if channel['id'] == channel_id:
                return channel
        return None
    #-------------------------------------------------------------------------#

    def get_chats(self) -> list:
        """Get list of all chats with their metadata"""
        return self.chats

    def get_chat_ids(self) -> list:
        """Get list of just the chat IDs"""
        return [chat['id'] for chat in self.chats]
        
    def get_telegram_chats(self) -> list:
        """Get list of Telegram chat IDs"""
        return [chat['id'] for chat in self.chats]

    def get_youtube_channels(self) -> list:
        """Get list of YouTube channels to monitor"""
        return self.channels

    def list_all(self):
        """Print current configuration details"""
        print("\n=== Current Configuration ===")
        print(f"Data folder: {self.data_folder}")
        print(f"Chats file: {self.chats_file}")
        print(f"Channels file: {self.channels_file}")
        
        print(f"\nMonitored YouTube Channels ({len(self.channels)}):")
        for channel in self.channels:
            print(f"- {channel['name']} (ID: {channel['id']})")
        
        print(f"\nConfigured Telegram Chats ({len(self.chats)}):")
        if not self.chats:
            print("No chats configured")
        else:
            for chat in self.chats:
                print(f"- {chat['title']} (ID: {chat['id']})")
                print(f"  Type: {chat['type']}")
                print(f"  Added: {chat['added_at']}")
        print("="*30 + "\n")