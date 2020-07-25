#!/usr/bin/env python3
import json
import re
from pprint import pprint

import requests
from requests.auth import HTTPBasicAuth

import credentials

auth = HTTPBasicAuth(credentials.user, credentials.token)
re_github = re.compile(r"^https://github\.com/[^/]+/[^/]+/?")


def getGithubStars(github_url):
    api_url = github_url.replace("https://github.com/", "https://api.github.com/repos/")
    if api_url[-1] == "/":
        api_url = api_url[:-1]
    r = requests.get(api_url, auth=auth)
    if r.status_code != 200:
        return None
    data = r.json()
    if "stargazers_count" not in data:
        print("Something went wrong: ", data)
        return None
    return data["stargazers_count"]


def updatestars(allscripts):
    for script in allscripts:
        stars = None
        github_url = re_github.match(script["url"])
        if github_url:
            stars = getGithubStars(github_url.group())
            own = github_url.group() == script["url"]
        if stars:
            print("got stars:", stars, own)
            script["stars"] = stars
            script["own"] = own
        # TODO: add gist and gitlab
    return allscripts


if __name__ == "__main__":
    with open("mpvscripts.json") as f:
        allscripts = json.load(f)

    allscripts = updatestars(allscripts)
    pprint(allscripts)

    with open("mpvscripts.json", "w") as f:
        json.dump(allscripts, f, indent=4)
