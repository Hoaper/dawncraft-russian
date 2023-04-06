import json
import os


def write_translation(pth: str, context):
    print(f"> Writing: {pth}...")
    with open(pth, "w", encoding="utf8") as f:
        json.dump(context, f, ensure_ascii=False)
    print("> Done")


def make_translation_fixes(text: str):
    colors = [["$(Red)", "$(red)"]]
    for color_ru, color_eng in colors:
        while color_ru in text:
            text = text.replace(color_ru, color_eng)
    return text


i = 1
first = True
for root, dirs, files in os.walk('quests'):
    if first:
        first = False
        continue
    for file in files:
        path = root + "\\" + file
        print(f"{i}) File: {path}...")
        with open(path, "r", encoding='utf8') as f:
            json_file = json.load(f)
            json_file["start"]["title"]["text"] = make_translation_fixes(json_file["start"]["description"]["text"])
            print(f'     ["start"]["title"]["text"]>>> {json_file["start"]["title"]["text"]}')
            json_file["start"]["description"]["text"] = make_translation_fixes(json_file["start"]["description"]["text"])
            print(f'     ["start"]["description"]["text"]>>> {json_file["start"]["description"]["text"]}')
            if "complete" in json_file:
                json_file["complete"]["title"]["text"] = make_translation_fixes(json_file["complete"]["title"]["text"])
                print(f'     ["complete"]["title"]["text"]>>> {json_file["complete"]["title"]["text"]}')
                json_file["complete"]["description"]["text"] = make_translation_fixes(json_file["complete"]["description"]["text"])
                print(f'     ["complete"]["description"]["text"]>>> {json_file["complete"]["description"]["text"]}')

            write_translation(path, json_file)
            i += 1
