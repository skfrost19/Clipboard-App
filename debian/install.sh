#!/bin/bash

# Install the clipboard-app.deb
sudo dpkg -i clipboard-manager.deb

# Prompt the user to add the app to the startup applications
echo "Do you want to add the clipboard app to the startup applications? [y/n]: "
read choice

if [[ $choice == "y" ]]; then
    # Add the app to the startup applications
    cp /usr/share/applications/clipboard-app.desktop ~/.config/autostart/
    echo "Clipboard app added to the startup applications."
else
    # Don't add the app to the startup applications
    echo "Clipboard app not added to the startup applications."
fi
