from button_modul import *

def fix_path(path):
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

def add_and_create_profile_to_json(Nik, Password, path, json_path, json_name = 'Profile_Data.json'):

    full_output_path = fix_path(json_path) + "\\" + json_name

    parent_dir = os.path.dirname(full_output_path)
    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)

    profile_dict = {}
    if len(Nik)>1 and len(str(Password))>1:
        complete = True
        profile_dict[Nik] = {"Password" : fix_path(Password), "Video_path" : fix_path(path)}
    else:
        complete = False

    #Запись Ника пользователя, пароля и пути к папке проекта
    if not os.path.exists(full_output_path):
        with open(full_output_path, 'w', encoding="utf-8") as f:
            json.dump(profile_dict, f, ensure_ascii=False, indent=2)
    #Запись Нового профиля в существующий файл
    else:
        with open(full_output_path, 'r+', encoding="utf-8") as f:
            try:
                existing_dict = json.load(f)

                combined_data = existing_dict | profile_dict
                f.seek(0)
                json.dump(combined_data, f, ensure_ascii=False, indent=2)
            except json.JSONDecodeError:
                json.dump(profile_dict, f, ensure_ascii=False, indent=2)
    if complete:
        return True
    else:
        return False

