# 🐳 Docker Setup for YouTube Telegram Bot

This guide helps you run the YouTube Telegram Bot using Docker for easy deployment and management.

## 📋 Prerequisites

- Docker installed on your system
- Docker Compose (optional, but recommended)
- YouTube Data API key
- Telegram Bot token

## 🚀 Quick Start

### 1. Setup Environment Variables

Copy the environment template and add your API keys:

```bash
cp .env.template .env
```

Edit `.env` file with your actual values:
```bash
YOUTUBE_API_KEY=your_youtube_api_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
```

### 2. Run with Docker Compose (Recommended)

```bash
# Build and start the bot
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the bot
docker-compose down
```

### 3. Run with Docker directly

```bash
# Build the image
docker build -t youtube-telegram-bot .

# Run the container
docker run -d \
  --name yt-telegram-bot \
  --restart unless-stopped \
  --env-file .env \
  -v "$(pwd)/Pydata:/app/Pydata" \
  youtube-telegram-bot

# View logs
docker logs -f yt-telegram-bot

# Stop the bot
docker stop yt-telegram-bot && docker rm yt-telegram-bot
```

### 4. Use Management Script (Easiest)

We've included a convenient management script:

```bash
# Make it executable
chmod +x docker-manage.sh

# Interactive menu
./docker-manage.sh

# Or use direct commands
./docker-manage.sh build    # Build image
./docker-manage.sh run      # Run bot
./docker-manage.sh stop     # Stop bot
./docker-manage.sh logs     # View logs
./docker-manage.sh restart  # Restart bot
./docker-manage.sh setup    # Setup .env file
```

## 📁 File Structure

```
YouTube-Telegram-Notification-Bot/
├── Dockerfile              # Container definition
├── docker-compose.yml      # Multi-container setup
├── .dockerignore           # Files to exclude from build
├── .env.template           # Environment variables template
├── .env                    # Your actual environment variables
├── docker-manage.sh        # Management script
└── DOCKER.md              # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `YOUTUBE_API_KEY` | YouTube Data API v3 Key | Yes | - |
| `TELEGRAM_BOT_TOKEN` | Telegram Bot Token | Yes | - |
| `CHECK_INTERVAL` | Check interval in minutes | No | 5 |
| `THUMBNAILS_ENABLED` | Enable thumbnails by default | No | true |
| `NOTIFICATIONS_ENABLED` | Enable notifications by default | No | true |
| `DEBUG` | Enable debug mode | No | false |
| `TZ` | Timezone | No | UTC |

### Docker Compose Features

- **Automatic restarts**: Container restarts unless stopped manually
- **Resource limits**: CPU and memory limits for stability
- **Health checks**: Monitors bot health and restarts if needed
- **Volume mounting**: Persists bot data between container restarts
- **Network isolation**: Runs in isolated Docker network

### Data Persistence

The bot data is persisted through Docker volumes:
- `./Pydata:/app/Pydata` - Channel and chat configuration
- `./logs:/app/logs` - Application logs (optional)

## 🔍 Monitoring and Logs

### View Real-time Logs
```bash
# With docker-compose
docker-compose logs -f

# With docker directly
docker logs -f yt-telegram-bot
```

### Check Container Status
```bash
# With docker-compose
docker-compose ps

# With docker directly
docker ps | grep yt-telegram-bot
```

### Health Check
```bash
# Check health status
docker inspect yt-telegram-bot | grep -A 5 "Health"
```

## 🛠️ Troubleshooting

### Container Won't Start
1. Check environment variables in `.env`
2. Verify API keys are correct
3. Check logs: `docker-compose logs` or `docker logs yt-telegram-bot`

### Bot Not Receiving Updates
1. Verify Telegram bot token
2. Check network connectivity
3. Ensure bot is added to Telegram groups

### Permission Issues
1. Check file permissions: `ls -la Pydata/`
2. Ensure Docker has access to mounted volumes

### Resource Issues
1. Check container resources: `docker stats yt-telegram-bot`
2. Adjust limits in `docker-compose.yml` if needed

## 🔄 Updates and Maintenance

### Update Bot Code
```bash
# Stop current container
./docker-manage.sh stop

# Pull latest code (if using git)
git pull

# Rebuild and restart
./docker-manage.sh build
./docker-manage.sh run
```

### Backup Data
```bash
# Backup bot configuration
tar -czf backup-$(date +%Y%m%d).tar.gz Pydata/
```

### Clean Up
```bash
# Remove old images
docker image prune

# Remove stopped containers
docker container prune

# Full cleanup (careful!)
docker system prune -a
```

## 🌐 Deployment Options

### Local Development
Use `docker-compose.yml` for local testing and development.

### Production Server
1. Set up proper environment variables
2. Configure log rotation
3. Set up monitoring and alerts
4. Use Docker Swarm or Kubernetes for scaling

### Cloud Deployment
- **Google Cloud Run**: Use included cloud deployment scripts
- **AWS ECS**: Compatible with ECS task definitions
- **Azure Container Instances**: Deploy with ACI
- **DigitalOcean Apps**: Deploy as container app

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [YouTube Data API](https://developers.google.com/youtube/v3)
- [Telegram Bot API](https://core.telegram.org/bots/api)

---

Need help? Check the main README.md or open an issue on GitHub! 🚀