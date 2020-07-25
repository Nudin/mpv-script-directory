#!/usr/bin/env python3
import json
import re
from pprint import pprint

import requests
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth

import credentials

page = requests.get("https://github.com/mpv-player/mpv/wiki/User-Scripts")
soup = BeautifulSoup(page.content, "html.parser")
elements = soup.find(id="wiki-body").select("li, h2")

auth = HTTPBasicAuth(credentials.user, credentials.token)

re_github = re.compile(r"^https://github\.com/[^/]+/[^/]+/?")

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


def getGithubStars(github_url, own):
    api_url = "https://api.github.com/repos/" + github_url[19:]
    r = requests.get(api_url, auth=auth)
    if r.status_code != 200:
        return None
    data = r.json()
    if "stargazers_count" not in data:
        print("oups", data)
        return None
    stars = data["stargazers_count"]
    if own:
        return "%s" % stars
    else:
        return "(%s)" % stars


for script in allscripts:
    stars = None
    github_url = re_github.fullmatch(script["url"])
    if github_url:
        stars = getGithubStars(github_url.string, True)
    github_url = re_github.match(script["url"])
    if github_url:
        stars = getGithubStars(github_url.string, False)
    if stars:
        print("got stars:", stars)
        script["stars"] = stars
    # TODO: add gist and gitlab

pprint(allscripts)

with open("mpvscripts.json", "w") as f:
    f.write(json.dumps(allscripts, indent=4))
