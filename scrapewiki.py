#!/usr/bin/env python3
import json
import re
from pprint import pprint

import requests
from bs4 import BeautifulSoup

from querystars import re_gist, re_github, re_gitlab, updatestars

page = requests.get("https://github.com/mpv-player/mpv/wiki/User-Scripts")
soup = BeautifulSoup(page.content, "html.parser")
elements = soup.find(id="wiki-body").select("li, h2")

re_windows = re.compile(r"\b[wW]indows\b")
re_linux = re.compile(r"\b[lL]inux\b")
re_mac = re.compile(r"\bmac(os|\b)", re.IGNORECASE)
re_unix = re.compile(r"\*nix|Unix")
re_proto = re.compile(r"^https?://")
re_domain_file = re.compile(r"^https?://([^/]*)/(?:[^#&]*/)*([^/#&]+)/?(?:#.*|&.*)*$")


def generateId(name, url):
    match = re_github.fullmatch(url)
    if match:
        return "github:" + "/".join(match.groups("")).rstrip("/")
    match = re_gitlab.fullmatch(url)
    if match:
        return "gitlab:" + "/".join(match.groups("")).rstrip("/")
    match = re_gist.fullmatch(url)
    if match:
        return "gist:" + "/".join(match.groups("")).rstrip("/")
    match = re_domain_file.fullmatch(url)
    if match:
        domain = match.groups()[0]
        filename = match.groups()[1]
        return f"{domain}:{filename}"
    return "XXX"  # FIXME


def uniquefy(identifier, name, test):
    unique = identifier
    if unique in test:
        unique = f"{identifier}/{name}"
        alt = f"{identifier}/{test[identifier]['name']}"
        test[alt] = test.pop(identifier)
        counter = 2
        while unique in test:
            unique = f"{identifier}-{counter}"
            counter += 1
    return unique


def extractText(element):
    texts = element.find_all(text=True)
    return "".join(texts[1:]).strip()


def normalizeType(type):
    type = type.lower()
    if type[-1] == "s":
        type = type[:-1]
    if type == "c plugin":
        type = "C plugin"
    return type


allscripts = {}
for entry in elements:
    if entry.name == "h2":
        type = entry.text.strip()
        continue
    a = entry.find("a")
    if a is None:
        continue
    name = entry.find("a").text
    url = entry.find("a").attrs["href"]
    script = {}
    scriptID = uniquefy(generateId(name, url), name, allscripts)
    script["name"] = name
    script["url"] = url
    script["type"] = normalizeType(type)
    p = entry.find("p")
    if p:
        desc = extractText(p)
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
    allscripts[scriptID] = script

allscripts = updatestars(allscripts)

pprint(allscripts)

with open("mpv_script_directory.json", "w") as f:
    json.dump(allscripts, f, indent=4)
