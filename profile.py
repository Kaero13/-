import json
import os


def fix_path(path)
    if path is None:
        return None
    elif path.startswith('"') and path.endswith('"'):
        path = path[1:-1]
    if "\\" in path:
        path = path.replace("\\", "/")

    try:
        return os.path.normpath(path)
    except:
        return path

def add_and_create_profile_to_json(Nik, Password, path, json_path, json_name = 'Profile_Data.json')
    pass
