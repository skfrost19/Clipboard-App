Steps to build a package :-

Necessary library/tools :-

- pip3 install PyQt5 Pyinstaller
- sudo apt install ruby
- gem install fpm --user-install (If you see a warning e.g. You don't have /home/martin/.local/share/gem/ruby/2.7.0/bin in your PATH you will need to add that to your path in your .bashrc file. check fpm --version)

Next, use pyinstaller and fpm to build a deb file (run the following in the terminal, also make sure to grant executables write to sh files.) :-

- pyinstaller Clipboard-App.spec
- ./package.sh
- fpm
