# Factorio Discord Bot

[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)

![Header Image][header-image.png]


We are coding this bot as far of the Discord Hack Week. It allows a server to play and control a character in Factorio from a discord channel as a collaborative experience. 

A large group of users should be able to each send commands to a Factorio character and together build the world.

This bot is a bit of a hack.

# Features
## Factorio Interactions
- [x] Player movement
- [x] Craft items
- [x] Place items
- [x] Pick up items
- [x] Send chat message
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
4. Start up a Factorio fullscreen and open/create a save.
5. Run main.py (FactorioBot directory)
6. Enjoy!

# Technical
![Component Diagram][technical-diagram.png]

## Journey
We originally looked at having the bot communicate directly with a Factorio mod over a internet connection similar to here [Clusterio](https://github.com/Danielv123/factorioClusterio) and the concept in this [reddit](https://www.reddit.com/r/factorio/comments/5g3qiz/modding_how_to_make_internet_connected_mods_like/) post.

They work through RCON and writing to a log file. 
However we quickly found that movement through the Factorio lua api would be extremely difficult to implement. To solve this challenge, we decided to make python act as a macro: directing keyboard and mouse inputs to Factorio allowed us to implement walking very easily.

A fun challenge we encountered: commands to control Factorio were running at the same time and conflicting with each other. To solve this we designed a command queue which queue the commands from users asynchronously until all previous commands have been run.

Next we started work on a Lua mod as that was required to allow us to craft items and complete other task in the game, such as setting research and placing items. We had some initial challenges: learning the api and how to interact with it. We again explored RCON to communicate with the Lua api and also hacking on_console_chat however both options were messy. After further research we discovered that we could add custom commands, which we could trigger from pyautogui.  

To return data back to the python bot we use a method seen in [Clusterio](https://github.com/Danielv123/factorioClusterio) of logging output to `script-output/` and then reading it from our code. Here we had to implement a file watch using the library `watchdog` to fix a race condition where discord read the log file before our mod wrote it.

Needless to say, this thing was a giant race condition.

## Current state
### Discord Bot
* `factoriocontrol.py`
    * Contains the command queue which has the `enqueue` function to add commands to the end of the queue. The command queue is non blocking so other commands from discord can be still handled and added to it. The first function has the command name and then in the command queue you pass in the function with `exec` in front of it (for example `exec_walk`) which is the function called when it is at the top of the command queue.
    * Contains all the discord.py commands which register on the command queue and are called by user to control factorio.
        * !walk
        * !craft
        * !say
        * !place
        * !pick_up
        * !research
        * !view_inventory
        * !view_tech
        * !output_command_queue
* `factoriohelper.py`
    * Contains user commands which are not bound to command queue so can be called and immediately executed at any time.
        * !help
        * !crafting_help
        * !research_help
        * !config
* `helper.py`
    * Contains helper functions for the cogs.
    * `SendFactorioCommand` calls `setup_read_txt` and then types a command using `pyautogui` into factorio to trigger the lua mod and then calls `read_ouput_txt` to get log from Factorio and returns that.
        * `setup_read_txt` sets up a file watch on `output.txt` and returns a observer.
        * `read_ouput_txt` waits for the watch and then read the full file safely and returns it.
    * `get_valid_direction` takes in a input and returns a valid single character direction or `None` if none exists.
      * `setup_config` creates a JSON file with default settings for cooldowns
      * `get_config` returns a cooldown configuration for a specific key (command/group) from the JSON config
      * `set_config` changes an attribute in a cooldown configuration for a specific key in the JSON config
     

[header-image.png]: https://cdn.discordapp.com/attachments/407617128112324629/594294628031922192/bot_banner.png
[technical-diagram.png]: https://i.imgur.com/cyJ808U.png


