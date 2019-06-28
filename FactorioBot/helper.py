import os
import asyncio
import re

import FactorioBot.config as config
import pyautogui as p
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


def get_valid_direction(input_str: str, sub_direction: bool = False):
    input_str = input_str.lower().strip()
    print(input_str)
    input_str = re.sub('[^a-z0-9]+', '', input_str)
    print(input_str)
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
