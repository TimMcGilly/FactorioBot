import os
import asyncio
import re

import json
import FactorioBot.config as config
import pyautogui as p
import logging
from discord.ext import commands
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


async def SendFactorioCommand(command: str, *args):
    observer: Observer = setup_read_txt()
    p.press("`")
    p.typewrite("/" + command + " " + " ".join(args), interval=0)
    p.press("enter")
    output = await read_ouput_txt(observer)
    return output


def setup_read_txt():
    dirpath = config.factorio_user_data + "\script-output"
    dirpath = os.path.expandvars(dirpath)
    path = dirpath + '\output.txt'

    if os.path.exists(path):
        observer = Observer()
        read_on_modified = ReadOnModified(path, observer)
        observer.schedule(read_on_modified, dirpath, recursive=False)
        observer.start()
        return observer


async def read_ouput_txt(observer: Observer):
    path = config.factorio_user_data + '\script-output\output.txt'
    path = os.path.expandvars(path)

    while observer.isAlive() is True:
        await asyncio.sleep(0.1)
    with open(path) as fp:
        return fp.read()


class ReadOnModified(FileSystemEventHandler):

    def __init__(self, file_to_check, observer):
        self.file_to_check = file_to_check
        self.observer = observer

    def on_modified(self, event):
        super(ReadOnModified, self).on_modified(event)

        if event.src_path == self.file_to_check:
            self.observer.stop()


def get_valid_direction(input_str: str, sub_direction: bool = False):
    input_str = input_str.lower().strip()
    input_str = re.sub('[^a-z0-9]+', '', input_str)
    valid_direction = None

    if input_str == "north" or input_str == "n":
        valid_direction = "n"
    elif input_str == "south" or input_str == "s":
        valid_direction = "s"
    elif input_str == "west" or input_str == "w":
        valid_direction = "w"
    elif input_str == "east" or input_str == "e":
        valid_direction = "e"

    if sub_direction:
        if input_str == "northwest" or input_str == "nw":
            valid_direction = "nw"
        elif input_str == "northeast" or input_str == "ne":
            valid_direction = "ne"
        elif input_str == "southwest" or input_str == "sw":
            valid_direction = "sw"
        elif input_str == "southeast" or input_str == "se":
            valid_direction = "se"

    return valid_direction


def setup_config():
    if not os.path.exists("config.json"):
        json_config = json.loads("""{
            "commands": {
                "walk": {
                    "uses": 2,
                    "cooldown": 15
                },
                "say": {
                    "uses": 2,
                    "cooldown": 5
                },
                "craft": {
                    "uses": 1,
                    "cooldown": 10
                },
                "research": {
                    "uses": 1,
                    "cooldown": 1
                },
                "place": {
                    "uses": 3,
                    "cooldown": 1
                },
                "view_gui":{
                    "uses": 1,
                    "cooldown": 15
                }
            }
        }
        """)
        with open('config.json', 'w') as outfile:
            json.dump(json_config, outfile)


def get_config(command_name):
    with open("config.json", 'r') as json_file:
        json_config = json.load(json_file)
        return [json_config['commands'][command_name]['uses'], json_config['commands'][command_name]['cooldown'],
                commands.BucketType.user]


def set_config(command_name, attribute, value):
    with open("config.json", 'r') as json_file:
        json_config = json.load(json_file)
    with open("config.json", 'w') as json_file:
        json_config['commands'][command_name][attribute] = value
        json.dump(json_config, json_file)
