import FactorioBot.config as config
import shutil
import os
import json

dirname = os.path.dirname(__file__)
dirname = os.path.join(dirname, "FactorioMod")

with open(dirname + r"\info.json", 'r') as json_file:
        json_config = json.load(json_file)
new_dirname = json_config['name'] + "_" + json_config['version']
rel_dirpath = os.path.join(r'\mods', new_dirname)
factoriopath = os.path.expandvars(config.factorio_user_data)
modpath = factoriopath + rel_dirpath

shutil.copytree(dirname, modpath)
