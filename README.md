# Clipboard App

- This is a GUI application built using PyQt5 which keeps track of the user's clipboard history.
- Build mainly for linux users.
- The app is designed to run in the background and can be accessed through the system tray icon.

![Clipboard Manager](https://github.com/skfrost19/Clipboard-App/blob/package/Demo/clipboard.png?raw=true)

## Requirements

- Python 3.7 or higher
- PyQt5

## Installation

- Clone the repository: `git clone https://github.com/skfrost19/Clipboard-App.git`
- Install the required dependencies:

  - For Windows: `pip install -r requirements.txt`
  - For linux: `pip3 install -r requirements.txt`

- Run the application:

  - Windows: `python clipboard.py`
  - Linux: `python3 clipboard.py`

- Packages for various linux flavours can also be retrieved from the [releases](https://github.com/skfrost19/Clipboard-App/releases/tag/v1.0.0) page.

## Build

- To build the application from source, run the following command:

  - clone the repo
  - checkout to the **package** branch `git checkout package`
  - follow the [Instruction](https://github.com/skfrost19/Clipboard-App/blob/package/README.md) to build the application

## Usage

- Once the application is running, it will automatically keep track of the user's clipboard history.
- To access the application, click on the system tray icon.
- The clipboard history will be displayed in a table with two columns: "Copied Elements" and "Options".
- The "Copied Elements" column displays the text that has been copied to the clipboard, and the "Options" column provides options for the user to interact with the clipboard history.

The user can clear the clipboard history by clicking the "Clear Clipboard" button at the bottom of the window. To exit the application, right-click on the system tray icon and select "Exit" from the context menu.

## Features

- Automatic clipboard tracking
- Display clipboard history in a table.
- Clear clipboard history
- Hide the application to the system tray on startup

## License

This project is licensed under the [MIT](LICENSE.txt) License.
