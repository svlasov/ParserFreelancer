#!/usr/bin/env python3
"""
Module Docstring
"""
import collections
from collections import Counter
from queue import Queue

import pytz
import requests
import gzip
import json
from datetime import datetime

from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from bs4 import BeautifulSoup

SKILLS_URLS_FILE = "data/skill_links.json"
# failures = 0

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

skill_urls_queue = Queue()

jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///scheduled_jobs.sqlite')
}
executors = {
    'default': {'type': 'threadpool', 'max_workers': 1}
}
job_defaults = {
    'coalesce': False,
    'max_instances': 1,
    'misfire_grace_time': 10
}

scheduler = BlockingScheduler(executors=executors, job_defaults=job_defaults, timezone=pytz.UTC)

def print_summary():
    print(f"total jobs fetched: {counters['jobs']}")


def fetch_jobs():

    url = skill_urls_queue.get()

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
            skill_urls_queue.put(url)

        scheduler.add_job(fetch_jobs,
                          next_run_time=datetime.utcnow(),
                          trigger=IntervalTrigger(seconds=10))

        scheduler.start()


def main():
    # load skill links from json file
    try:
        poll_jobs_by_skills_json()
    except KeyboardInterrupt:
        print_summary()
    print_summary()


if __name__ == "__main__":
    main()
