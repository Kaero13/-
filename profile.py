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
    full_output_path = os.path.dirname(json_path, json_name)

    parent_dir = os.path.dirname(full_output_path)
    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)

    profile_dict = {}
    profile_dict[Nik] = {"Password" : Password, "Video_path" : path}

    if not os.path.exists(json_path):
        with open(full_output_path, 'w', encoding="utf-8") as f:
            json.dump(profile_dict, f, ensure_ascii=False, indent=2)

    else:
        pass
