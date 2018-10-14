#!/usr/bin/env python3
"""
Module Docstring
"""
from collections import Counter
import requests
import gzip
import json
from datetime import datetime
from bs4 import BeautifulSoup

SKILLS_URLS_FILE = "data/skill_links.json"
#failures = 0

# class Skill:
#     key: str
#     disp: str


# class Job:
#     title: str
#     url: str
#     desc: str
#     created_at: datetime
#     skills: [Skill]

counters = Counter()

def print_summary():
    print(f"total jobs fetched: {counters['jobs']}")

def fetch_jobs(url):

    print(f"fetching latest jobs from {url}")

    resp = requests.get(url)
    
    if not resp.ok:
        raise RuntimeError(f"failed to fetch {url}")

    else:
        soup = BeautifulSoup(resp.text)
        
        job_elems = soup.select("#project-list .JobSearchCard-item-inner")
        print(job_elems)

        job_doc = {}

        for job_elem in job_elems:

            counters['jobs'] += 1

            title_elems = job_elem.select("a.JobSearchCard-primary-heading-link")
            
            if not title_elems:
                counters['failures'] += 1
                print("title elems not found...")
                continue
            else:
                title_elem = title_elems[0]
                stripped_title_strings = list(title_elem.stripped_strings)
                if not stripped_title_strings:
                    counters['failures'] += 1
                    print("could not extract title text...")
                    continue
                else:
                    title = stripped_title_strings[0]
                    print(f"title: {title}")
                    job_doc['title'] = title
    

def poll_jobs_by_skills_json():

    with open(SKILLS_URLS_FILE) as fp:
        urls = json.load(fp)
        print(f"total {len(urls)} urls")
        
        for url in urls:
            try:
                fetch_jobs(url)
            except RuntimeError as err:
                #print(err)
                counters['failures'] += 1
                print(f"failed to fetch {url}")
                if counters['failures'] >= 3:
                    print(err)
                    break

def main():
    
    # load skill links from json file
    try:
        poll_jobs_by_skills_json()
    except KeyboardInterrupt as ctrl_c:
        print_summary()
    print_summary()
    

if __name__ == "__main__":
    main()
