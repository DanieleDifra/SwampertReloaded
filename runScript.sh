#!/bin/bash

if ps -C python >/dev/null; then
    echo "TelegramBot is already running."
else
    echo "Booting TelegramBot"
    sleep 5m 
    python /home/swampi/SwampertReloaded/telegramBot.py >> botLogs.txt
fi

