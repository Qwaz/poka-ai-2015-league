import json
import subprocess

def parse_setting():
    setting_file = open('setting.json', 'r')
    return json.loads(setting_file.read())

setting = parse_setting()
print(setting)
