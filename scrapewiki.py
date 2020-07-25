#!/usr/bin/env python3
import json
import re
from pprint import pprint

import requests
from bs4 import BeautifulSoup

from querystars import updatestars

page = requests.get("https://github.com/mpv-player/mpv/wiki/User-Scripts")
soup = BeautifulSoup(page.content, "html.parser")
elements = soup.find(id="wiki-body").select("li, h2")

re_windows = re.compile(r"\b[wW]indows\b")
re_linux = re.compile(r"\b[lL]inux\b")
re_mac = re.compile(r"\bmac(os|\b)", re.IGNORECASE)
re_unix = re.compile(r"\*nix|Unix")

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
        desc = p.find_all(text=True)[-1].strip()  # FIXME
        script["desc"] = desc
        script["os"] = []
        if re_linux.search(desc):
            script["os"].append("Linux")
        if re_windows.search(desc):
            script["os"].append("Windows")
        if re_mac.search(desc):
            script["os"].append("Mac")
        if re_unix.search(desc):
            script["os"] += ["Linux", "Mac"]
    allscripts.append(script)

allscripts = updatestars(allscripts)

pprint(allscripts)

with open("mpvscripts.json", "w") as f:
    json.dump(allscripts, f, indent=4)
