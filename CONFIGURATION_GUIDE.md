# Configuration Guide

## Overview
The bot now uses `configuration.json` to manage notification settings. These settings are automatically loaded and merged into the bot's internal settings.

## Configuration File Location
`Pydata/configuration.json`

## Current Settings

### Notification Settings
```json
{
  "notification_settings": {
    "thumbnails": false,
    "link_preview": false,
    "link_preview_settings": {
      "preferred_small_photo": false,
      "preferred_large_photo": false,
      "show_text_above": false
    }
  },
  "show_in_status_notify": true
}
```

### Setting Descriptions

#### thumbnails
- **Type**: Boolean
- **Default**: `false`
- **Description**: Controls whether video thumbnail images are sent with notifications
- **Effect**: 
  - `true`: Notifications include thumbnail images
  - `false`: Text-only notifications (uses link preview instead)

#### link_preview
- **Type**: Boolean
- **Default**: `false`
- **Description**: Controls whether Telegram's link preview is enabled for video URLs
- **Effect**:
  - `true`: Link previews are enabled (is_disabled = false)
  - `false`: Link previews are disabled (is_disabled = true)

#### link_preview_settings

##### preferred_small_photo
- **Type**: Boolean
- **Default**: `false`
- **Description**: Shrinks media in the link preview
- **Maps to**: `prefer_small_media` in Telegram API

##### preferred_large_photo
- **Type**: Boolean
- **Default**: `false`
- **Description**: Enlarges media in the link preview
- **Maps to**: `prefer_large_media` in Telegram API

##### show_text_above
- **Type**: Boolean
- **Default**: `false`
- **Description**: Shows the link preview above the message text
- **Maps to**: `show_above_text` in Telegram API

#### show_in_status_notify
- **Type**: Boolean
- **Default**: `true`
- **Description**: Whether to display these settings in the `/status_notify` command output

## How It Works

1. **On Bot Startup**:
   - Bot loads `configuration.json`
   - Settings are merged into `settings.json`
   - Bot uses the merged settings for all operations

2. **Configuration Priority**:
   - `configuration.json` → Primary source
   - `settings.json` → Fallback and runtime storage
   - Command-based changes override both (saved to `settings.json`)

3. **Viewing Current Settings**:
   - Use `/status_notify` command to see active settings
   - Shows both thumbnails and link preview configurations

## Commands Related to Configuration

### Thumbnail Control
- `/enable_thumbnails` - Enable thumbnail images in notifications
- `/disable_thumbnails` - Disable thumbnails (uses link preview)

### Link Preview Control
- `/set_link_preview <option> <true|false>` - Configure link preview options
  - Options: `disabled`, `small`, `large`, `above`
  - Example: `/set_link_preview small true`

### Status Check
- `/status_notify` - Shows current configuration and bot status

## Modifying Configuration

### Method 1: Edit configuration.json (Recommended)
1. Edit `Pydata/configuration.json`
2. Restart the bot
3. Settings will be automatically loaded

### Method 2: Use Bot Commands
1. Use commands like `/enable_thumbnails` or `/set_link_preview`
2. Changes are saved to `settings.json`
3. Persists across restarts

### Method 3: Edit settings.json Directly
1. Edit `Pydata/settings.json`
2. Restart the bot
3. Changes take effect immediately

## Examples

### Example 1: Enable Thumbnails with Small Link Preview
```json
{
  "notification_settings": {
    "thumbnails": true,
    "link_preview": true,
    "link_preview_settings": {
      "preferred_small_photo": true,
      "preferred_large_photo": false,
      "show_text_above": false
    }
  }
}
```

### Example 2: Text-Only with No Link Preview
```json
{
  "notification_settings": {
    "thumbnails": false,
    "link_preview": false,
    "link_preview_settings": {
      "preferred_small_photo": false,
      "preferred_large_photo": false,
      "show_text_above": false
    }
  }
}
```

### Example 3: Text-Only with Large Link Preview Above Text
```json
{
  "notification_settings": {
    "thumbnails": false,
    "link_preview": true,
    "link_preview_settings": {
      "preferred_small_photo": false,
      "preferred_large_photo": true,
      "show_text_above": true
    }
  }
}
```

## Troubleshooting

### Settings Not Taking Effect
1. Check that `configuration.json` is in the `Pydata` folder
2. Verify JSON syntax is correct
3. Restart the bot
4. Check bot logs for configuration loading messages

### Settings Reset to Default
- If `configuration.json` is missing or invalid, default settings are used
- Check for JSON syntax errors
- Ensure file permissions allow reading

### Command Changes Not Persisting
- Commands save to `settings.json`, not `configuration.json`
- To make permanent changes, update `configuration.json`

## Notes

- Settings are case-sensitive
- Boolean values must be `true` or `false` (lowercase, no quotes)
- Invalid JSON will cause the bot to use default settings
- The bot logs configuration loading status on startup
