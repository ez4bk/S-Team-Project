import json

f = open('config.json')
config = json.load(f)

f.close()


def write_to_json():
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)
