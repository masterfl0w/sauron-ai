#!/bin/bash

# Configuration
PROJECT_DIR="/Users/floriangrima/Desktop/projets/sauron-ai"
PYTHON_BIN="/Users/floriangrima/.pyenv/versions/3.13.0/bin/python3"
PLIST_PATH="$HOME/Library/LaunchAgents/com.sauron.service.plist"
USER_ID=$(id -u)

# 1. Create the LaunchAgent PLIST
# Moving logs to /tmp to avoid potential Desktop permission issues with launchd
cat <<EOF > "$PLIST_PATH"
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.sauron.service</string>
    <key>ProgramArguments</key>
    <array>
        <string>$PYTHON_BIN</string>
        <string>$PROJECT_DIR/backend/api.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>WorkingDirectory</key>
    <string>$PROJECT_DIR</string>
    <key>StandardOutPath</key>
    <string>/tmp/sauron-backend.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/sauron-backend.log</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PYTHONPATH</key>
        <string>$PROJECT_DIR/sdk</string>
    </dict>
</dict>
</plist>
EOF

chmod 644 "$PLIST_PATH"
echo "✅ Created LaunchAgent at $PLIST_PATH"

# 2. Register and start the service
launchctl bootout gui/$USER_ID "$PLIST_PATH" 2>/dev/null
launchctl bootstrap gui/$USER_ID "$PLIST_PATH"

echo "🚀 Sauron Background Service bootstrapped."
echo "Checking status..."
sleep 2
launchctl list com.sauron.service

echo "------------------------------------------------"
echo "API/UI:    http://127.0.0.1:8000"
echo "Logs:      tail -f /tmp/sauron-backend.log"
