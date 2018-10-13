import datetime
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from selenium import webdriver

from mongodb_persist import db, skills_coll, jobs_coll

SKILL_BASE_URL = "https://www.freelancer.com/jobs/"

def work(skill_key="python"):

    url = "{base_url}/{skill_key}/".format(base_url=SKILL_BASE_URL, skill_key=skill_key)

    driver.get(url)

    job_elems = driver.find_elements_by_css_selector("#project-list .JobSearchCard-item-inner")

    job_docs = []

    for job_elem in job_elems:

        job = {}

        title_elem = job_elem.find_element_by_css_selector("a.JobSearchCard-primary-heading-link")
        job['title'] = title_elem.text
        job['url'] = title_elem.get_attribute("href")

        days_left_elem = job_elem.find_element_by_css_selector("span.JobSearchCard-primary-heading-Days")
        job['days_left'] = days_left_elem.text

        description_elem = job_elem.find_element_by_css_selector("p.JobSearchCard-primary-description")
        job['description'] = description_elem.text

        skill_elems = job_elem.find_elements_by_css_selector("div.JobSearchCard-primary-tags a")

        job['skills'] = []


        for se in skill_elems:
            skill_url = se.get_attribute("href")

            skill_key = ""

            if skill_url and skill_url.startswith(SKILL_BASE_URL):
                skill_key = skill_url[len(SKILL_BASE_URL):-1]

            skill = {
                'skill': se.text,
                'skill_url': skill_url,
                'skill_key': skill_key
            }

            job['skills'].append(skill)

        print("job: {}".format(job))

        job_docs.append(job)

    return job_docs


def save_jobs(job_docs):
    for job_doc in job_docs:
        job_doc["_id"] = job_doc["url"]
        try:
            job_skill_docs = job_doc['skills']

            for skill_doc in job_skill_docs:

                if skill_doc['skill_key'] not in all_skill_keys:
                    all_skill_keys.add(skill_doc['skill_key'])

                    skills_coll.insert(skill_doc)

            job_doc['created_at'] = datetime.datetime.utcnow()
            jobs_coll.insert(job_doc)
        except DuplicateKeyError as dup_err:
            print("pk {} already exists".format(job_doc["_id"]))


if __name__ == "__main__":


    t0 = datetime.datetime.utcnow()
    driver = webdriver.Firefox()

    all_skill_keys = set([d['skill_key'] for d in skills_coll.find()])
    interesting_skill_keys = ["python"]
                              #   , "javascript",
                              # "test-automation", "testing-qa",
                              # "amazon-web-services",
                              # "web-scraping", "mysql"]#all_skill_keys.copy()

    try:
        for sk in interesting_skill_keys:
            job_docs = work(skill_key=sk)
            save_jobs(job_docs)
    except Exception as ex:
        print(ex)
    finally:
        t1 = datetime.datetime.utcnow()
        # print(t1 - t0)
        driver.close()