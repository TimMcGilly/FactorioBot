# Factorio Discord Bot

[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)

![Header Image][header-image.png]


We are coding this bot as far of the Discord Hack Week. It allows a server to play and control a character in factorio from a discord channel as a collaborative experience. 

A large group of users should be able to each send commands to a factorio character and together build the world.

This bot is a bit of a hack.

# Planned features
## Factorio Interactions
- [x] Player movement
- [x] Craft items
- [x] Place items
- [ ] Pick up items
- [x] Send game chat message
- [x] Set research
- [x] View inventory and tech tree GUI's 
## Additional features
- [x] Take screenshots  
- [x] Customisable command cooldowns
- [x] Tasks executed in a queue
- [x] Order of the queue displayed upon request
- [x] Help commands where item/tech names are required
    
# Setup
## Dependencies
- `python 3.6 or higher`
- `discord.py`
- `pyautogui`
- `watchdog`

## Install
```commandline
git clone https://github.com/TotallyCoded/FactorioBot.git
cd FactorioBot\FactorioBot
pip install requirements.txt
```

# Usage
1. Create an application and bot at https://discordapp.com/developers/applications/
2. Create a `config.py` file with:

    ```py
    token = "token-here"
    factorio_user_data='%Appdata%\Factorio-or-your-folder-here'
    ```
3. Run setup.py (this will install the supplied bridge mod)
4. Start up a factorio fullscreen and open/create a save.
5. Run main.py (FactorioBot directory)
6. Enjoy!

[header-image.png]: https://i.imgur.com/ZW2V92t.png


