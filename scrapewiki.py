#!/usr/bin/env python3
import json
from pprint import pprint

import requests
from bs4 import BeautifulSoup

from querystars import updatestars

page = requests.get("https://github.com/mpv-player/mpv/wiki/User-Scripts")
soup = BeautifulSoup(page.content, "html.parser")
elements = soup.find(id="wiki-body").select("li, h2")


allscripts = []
for entry in elements:
    if entry.name == "h2":
        language = entry.text.strip()
        continue
    a = entry.find("a")
    if a is None:
        continue
    script = {}
    script["name"] = entry.find("a").text
    script["url"] = entry.find("a").attrs["href"]
    p = entry.find("p")
    if p:
        script["desc"] = p.find_all(text=True)[-1].strip()
    allscripts.append(script)

allscripts = updatestars(allscripts)

pprint(allscripts)

with open("mpvscripts.json", "w") as f:
    json.dump(allscripts, f, indent=4)
