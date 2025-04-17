#!/usr/bin/env python3
import json
import os
import re
from functools import lru_cache
from pprint import pprint

import requests
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth

# It requires a Github personal access token with the "repo" scope
# to be set in the credentials.py file.
try:
    import credentials
except ImportError:

    class credentials:
        user = None
        # Fall back to env variable GITHUB_TOKEN
        token = os.getenv("GITHUB_TOKEN")


# This script queries the Github API for the number of stars of a repository
# and updates the mpv_script_directory.json file accordingly.


re_gitlab = re.compile(
    r"^https://gitlab\.com/([^/]+)/([^/]+)(?:/[^#&]*?)*?([^/#&]+)?/?(?:#.*|&.*)*$"
)
re_github = re.compile(
    r"^https://github\.com/([^/]+)/([^/]+)(?:/[^#&]*?)*?([^/#&]+)?/?(?:#.*|&.*)*$"
)
re_gist = re.compile(r"^https://gist.github\.com/([^/]+)/(\w+)/?(?:#.*|&.*)*$")


@lru_cache(maxsize=128)
def getGithubStars(owner, repo, _):
    auth = HTTPBasicAuth(credentials.user, credentials.token)
    api_url = f"https://api.github.com/repos/{owner}/{repo}"
    r = requests.get(api_url, auth=auth)
    if r.status_code != 200:
        return None
    data = r.json()
    if "stargazers_count" not in data:
        print("Something went wrong: ", data)
        return None
    return data["stargazers_count"]


def updatestars(allscripts):
    for script in allscripts.values():
        stars = None
        url = script["url"] or ""
        match = re_github.fullmatch(url)
        if match:
            stars = getGithubStars(*match.groups())
            if stars is None:
                print("dead url", url)
                script["url"] = None
                continue
            shared = match.groups()[2] is not None
        elif re_gist.match(url):
            # Github API is missing a possibility to query for stars of a gist
            page = requests.get(url)
            if page.status_code == 404:
                print("dead url", url)
                script["url"] = None
                continue
            soup = BeautifulSoup(page.content, "html.parser")
            stars = int(soup.select_one("#gist-star-button .Counter").text.strip())
            shared = False
        # Scraping gitlab.com doen't work anymore without javascript
        # TODO use gitlab api instead (if possible)
        # elif match := re_gitlab.match(url):
        #    page = requests.get(url)
        #    if page.status_code == 404:
        #        print("dead url", url)
        #        script["url"] = None
        #        continue
        #    soup = BeautifulSoup(page.content, "html.parser")
        #    stars = int(soup.select_one(".star-count").text.strip())
        #    shared = match.groups()[2] is not None
        if stars:
            print("got stars:", stars, shared, url)
            script["stars"] = stars
            script["sharedrepo"] = shared
    return allscripts


if __name__ == "__main__":
    with open("mpv_script_directory.json") as f:
        allscripts = json.load(f)

    allscripts = updatestars(allscripts)
    pprint(allscripts)

    with open("mpv_script_directory.json", "w") as f:
        json.dump(allscripts, f, indent=4)
