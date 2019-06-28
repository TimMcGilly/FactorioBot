import os
import asyncio
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