import datetime
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from selenium import webdriver


def work(skill_key="python"):

    url = "https://www.freelancer.com/jobs/{}/".format(skill_key)

    driver.get(url)

    # elem = driver.find_element_by_id("project-list")
    job_elems = driver.find_elements_by_css_selector("#project-list .JobSearchCard-item-inner")

    job_docs = []

    for job_elem in job_elems:
        # title = block.find('a', class_='JobSearchCard-primary-heading-link').contents[0]

        job = {}

        title_elem = job_elem.find_element_by_css_selector("a.JobSearchCard-primary-heading-link")
        job['title'] = title_elem.text
        job['url'] = title_elem.get_attribute("href")

        days_left_elem = job_elem.find_element_by_css_selector("span.JobSearchCard-primary-heading-Days")
        job['days_left'] = days_left_elem.text

        # description = block.find('p', class_='JobSearchCard-primary-description').contents[0]
        description_elem = job_elem.find_element_by_css_selector("p.JobSearchCard-primary-description")
        job['description'] = description_elem.text

        # skills_block = block.find('div', class_='JobSearchCard-primary-tags')
		# skills = skills_block.find_all('a')
        skill_elems = job_elem.find_elements_by_css_selector("div.JobSearchCard-primary-tags a")

        job['skills'] = []

        SKILL_BASE_URL = "https://www.freelancer.com/jobs/"

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

        #return job
        job_docs.append(job)

    return job_docs



# driver = webdriver.Chrome()

def save_jobs(job_docs):
    for job_doc in job_docs:
        job_doc["_id"] = job_doc["url"]
        try:
            job_skill_docs = job_doc['skills']

            for js_doc in job_skill_docs:

                if js_doc['skill_key'] not in all_skill_keys:
                    all_skill_keys.add(js_doc['skill_key'])
                    skills_coll.insert(js_doc)

            jobs_coll.insert(job_doc)
        except DuplicateKeyError as dup_err:
            print("pk {} already exists".format(job_doc["_id"]))


if __name__ == "__main__":

    db_host = 'localhost'
    db_name = "jobs"
    coll_name = "jobs"

    t0 = datetime.datetime.utcnow()
    driver = webdriver.Firefox()

    client = MongoClient(db_host)
    db = client[db_name]

    jobs_coll = db.get_collection(coll_name)
    skills_coll = db.get_collection("skills")

    all_skill_keys = set([d['skill_key'] for d in skills_coll.find()])
    all_skill_keys_copy = all_skill_keys.copy()

    try:
        for sk in all_skill_keys_copy:
            job_docs = work(skill_key=sk)
            save_jobs(job_docs)
    except Exception as ex:
        print(ex)
    finally:
        t1 = datetime.datetime.utcnow()
        print(t1 - t0)
        driver.close()