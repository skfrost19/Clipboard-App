#!/bin/bash

sudo dpkg --remove clipboard-manager

# Prompt the user to remove the app from the startup applications
echo "Do you want to remove the clipboard app from the startup applications? [y/n]"
read choice

if [[ $choice == "y" ]]; then
    # Remove the app from the startup applications
    rm ~/.config/autostart/clipboard-app.desktop
    echo "Clipboard app removed from the startup applications."
else
    # Don't remove the app from the startup applications
    echo "Clipboard app not removed from the startup applications."
fi