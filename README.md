#Factorio Discord Bot
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)

![Header Image][header-image.png]


We are coding this bot as far of the Discord Hack Week. It allows you to play and control a character in factorio from a discord channel as a collaborative experience. 

A large group of players should be able to each send the factorio players a few commands and together build the world.

##Planned features
- [ ] Player movement
- [ ] Take screenshots
- [ ] Craft items
- [ ] Place items
- [ ] Pick up items
- [ ] Send chat message
- [ ] Server controllable cooldowns

##Setup
### Dependencies
- `discord.py`
- `pyautogui`

### Install
```commandline
git clone https://github.com/TotallyCoded/FactorioBot.git
cd FactorioBot\FactorioBot
pip install requirements.txt
```

## Usage
1. Create an application and discord bot at https://discordapp.com/developers/applications/
2. Create a `config.py` file with:

    ```py
    token = "token-here"
    ```
3. Setup up factorio and have it as a open fullscreen window.

[header-image.png]: https://i.imgur.com/ZW2V92t.png


