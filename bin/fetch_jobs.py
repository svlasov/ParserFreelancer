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

counters = Counter()
job_counter = Counter()
skill_counter = Counter()


def print_summary():
    print(job_counter)
    print(skill_counter)

def fetch_jobs(url):

    print(f"fetching latest jobs from {url}")

    resp = requests.get(url)
    
    if not resp.ok:
        raise RuntimeError(f"failed to fetch {url}")

    else:
        soup = BeautifulSoup(resp.text)
        
        job_elems = soup.select("#project-list .JobSearchCard-item-inner")
        #print(job_elems)

        job_doc = {}

        for job_elem in job_elems:

            title_link = job_elem.select_one("a.JobSearchCard-primary-heading-link")
            job_doc['title'] = title_link.text.strip()
            job_doc['href'] = title_link.attrs.get('href')
            job_doc['desc'] = job_elem.select_one("p.JobSearchCard-primary-description").text.strip()

            job_counter[job_doc['href']] += 1

            # TODO: save job

            skill_links = job_elem.select("div.JobSearchCard-primary-tags a")

            for skill_link in skill_links:
                skill_text = skill_link.text.strip()
                skill_href = skill_link.attrs.get('href')

                # TODO: save skill
                skill_counter[skill_href] += 1
    

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
    except KeyboardInterrupt:
        pass
        # print_summary()
    finally:
        print_summary()
    

if __name__ == "__main__":
    main()
