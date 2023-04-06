import os
import json
import requests
import time

url = "https://translated-mymemory---translation-memory.p.rapidapi.com/get"


headers = {
    "X-RapidAPI-Key": "8339f53bf6mshd832999f806d0a3p1de879jsn23864d360f48",
    "X-RapidAPI-Host": "translated-mymemory---translation-memory.p.rapidapi.com"
}


def make_request(data: str):
    querystring = {
        "langpair": "en|ru",
        "q": data,
        "mt": "1",
        "onlyprivate": "0",
        "de": "a@b.c"
    }
    req = requests.request("GET", url, headers=headers, params=querystring)
    if req.status_code != 200:
        print(req.text, req.status_code, req, sep="\n\n")
        exit(-1)
    return req.json()['responseData']['translatedText']


def write_translation(pth: str, context):
    print(f"> Writing: {pth}...")
    with open(pth, "w", encoding="utf8") as f:
        json.dump(context, f, ensure_ascii=False)
    print("> Done")


i = 1
first = True
for root, dirs, files in os.walk('quests_eng'):
    if first:
        first = False
        continue
    for file in files:
        print(f"{i}) File: {file}...")
        path = root + "\\" + file
        with open(path, "r", encoding='utf8') as f:
            json_file = json.load(f)
            json_file["start"]["title"]["text"] = make_request(json_file["start"]["title"]["text"])
            json_file["start"]["description"]["text"] = make_request(json_file["start"]["description"]["text"])
            if "complete" in json_file:
                json_file["complete"]["title"]["text"]=make_request(json_file["complete"]["title"]["text"])
                json_file["complete"]["description"]["text"]=make_request(json_file["complete"]["description"]["text"])

            print(f"Translated version: {json_file}")

            write_translation(path, json_file)
            if i % 3 == 0:
                time.sleep(5)

        i += 1


