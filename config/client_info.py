import json
import os

from config.project_info import ROOT_DIR

f = open(os.path.join(ROOT_DIR, 'config.json'))
config = json.load(f)

f.close()


def write_to_json():
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)
