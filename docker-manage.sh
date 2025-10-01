#!/bin/bash

# Docker Setup and Deployment Script for YouTube Telegram Bot
# This script helps you build, run, and manage your bot with Docker

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Function to check if .env file exists
check_env_file() {
    if [ ! -f ".env" ]; then
        print_warning ".env file not found!"
        print_info "Copying .env.template to .env..."
        cp .env.template .env
        print_warning "Please edit .env file with your actual API keys before running the bot!"
        print_info "Required variables:"
        echo "  - YOUTUBE_API_KEY"
        echo "  - TELEGRAM_BOT_TOKEN"
        return 1
    fi
    return 0
}

# Function to build Docker image
build_image() {
    print_info "Building Docker image..."
    docker build -t youtube-telegram-bot:latest .
    print_success "Docker image built successfully!"
}

# Function to run with docker-compose
run_with_compose() {
    print_info "Starting bot with docker-compose..."
    docker-compose up -d
    print_success "Bot started successfully!"
    print_info "Use 'docker-compose logs -f' to view logs"
}

# Function to run with docker directly
run_with_docker() {
    print_info "Starting bot with Docker..."
    docker run -d \
        --name yt-telegram-bot \
        --restart unless-stopped \
        --env-file .env \
        -v "$(pwd)/Pydata:/app/Pydata" \
        youtube-telegram-bot:latest
    print_success "Bot started successfully!"
    print_info "Use 'docker logs -f yt-telegram-bot' to view logs"
}

# Function to stop the bot
stop_bot() {
    print_info "Stopping the bot..."
    
    # Try docker-compose first
    if [ -f "docker-compose.yml" ] && docker-compose ps | grep -q "youtube-telegram-bot"; then
        docker-compose down
    fi
    
    # Try direct docker container
    if docker ps | grep -q "yt-telegram-bot"; then
        docker stop yt-telegram-bot
        docker rm yt-telegram-bot
    fi
    
    print_success "Bot stopped!"
}

# Function to view logs
view_logs() {
    if docker-compose ps | grep -q "youtube-telegram-bot"; then
        docker-compose logs -f
    elif docker ps | grep -q "yt-telegram-bot"; then
        docker logs -f yt-telegram-bot
    else
        print_error "No running bot container found!"
    fi
}

# Function to restart the bot
restart_bot() {
    print_info "Restarting the bot..."
    stop_bot
    sleep 2
    if [ -f "docker-compose.yml" ]; then
        run_with_compose
    else
        run_with_docker
    fi
}

# Main menu
show_menu() {
    echo ""
    echo "🤖 YouTube Telegram Bot - Docker Management"
    echo "==========================================="
    echo "1. Build Docker image"
    echo "2. Run bot (docker-compose)"
    echo "3. Run bot (docker only)"
    echo "4. Stop bot"
    echo "5. View logs"
    echo "6. Restart bot"
    echo "7. Setup environment file"
    echo "8. Exit"
    echo ""
}

# Parse command line arguments
case "${1:-}" in
    "build")
        build_image
        ;;
    "run")
        check_env_file || exit 1
        if [ -f "docker-compose.yml" ]; then
            run_with_compose
        else
            build_image
            run_with_docker
        fi
        ;;
    "stop")
        stop_bot
        ;;
    "logs")
        view_logs
        ;;
    "restart")
        check_env_file || exit 1
        restart_bot
        ;;
    "setup")
        check_env_file
        ;;
    *)
        # Interactive mode
        while true; do
            show_menu
            read -p "Choose an option (1-8): " choice
            
            case $choice in
                1)
                    build_image
                    ;;
                2)
                    check_env_file || continue
                    run_with_compose
                    ;;
                3)
                    check_env_file || continue
                    build_image
                    run_with_docker
                    ;;
                4)
                    stop_bot
                    ;;
                5)
                    view_logs
                    ;;
                6)
                    check_env_file || continue
                    restart_bot
                    ;;
                7)
                    check_env_file
                    ;;
                8)
                    print_info "Goodbye!"
                    exit 0
                    ;;
                *)
                    print_error "Invalid option. Please choose 1-8."
                    ;;
            esac
            
            echo ""
            read -p "Press Enter to continue..."
        done
        ;;
esac