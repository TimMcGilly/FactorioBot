import os
import asyncio
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
    print(observer.isAlive())
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
                }
            }
        }
        """)
        print(json_config)
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
