#!/usr/bin/env python3
"""
Module Docstring
"""
import requests
import gzip
import json
from bs4 import BeautifulSoup

SKILLS_URL = "https://www.freelancer.com/sitemap/default/jobs-1.xml.gz"

def main():
    print(f"trying to fetch skills from {SKILLS_URL}")

    # fetch
    resp = requests.get(SKILLS_URL)

    # decompress
    xml = gzip.decompress(resp.content)

    # parse
    soup = BeautifulSoup(xml, features="html.parser")
    url_elems = soup.find_all("loc")
    urls = [elm.text for elm in url_elems]

    # write all links to a json file
    with open("data/skill_links.json", "w") as fp:
        json.dump(urls, fp)

    print(f"total {len(urls)} urls")


if __name__ == "__main__":
    main()
