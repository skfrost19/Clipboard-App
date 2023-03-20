#!/bin/bash
# create folders
[ -e package ] && rm -r package
mkdir -p package/opt
mkdir -p package/usr/share/applications
mkdir -p package/usr/share/icons/hicolor/scalable/apps

# copy files
cp -r dist/Clipboard-App package/opt/Clipboard-App
cp icon.png package/usr/share/icons/hicolor/scalable/apps/clipboard-app.png
cp clipboard-app.desktop package/usr/share/applications/clipboard-app.desktop

# change permissions
find package/opt/Clipboard-App -type f -exec chmod 644 {} +
find package/opt/Clipboard-App -type d -exec chmod 755 {} +
find package/usr/share -type f -exec chmod 644 {} +
chmod 777 package/opt/Clipboard-App/clipboard_history.pkl 
chmod +x package/opt/Clipboard-App/Clipboard-App