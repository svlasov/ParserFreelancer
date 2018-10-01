from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from collections import Counter

def work(category="python"):

    url = f"https://www.freelancer.com/jobs/{category}/"

    driver.get(url)

    # elem = driver.find_element_by_id("project-list")
    job_elems = driver.find_elements_by_css_selector("#project-list .JobSearchCard-item-inner")
    job_list = []

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
        job['skills'] = [se.text for se in skill_elems]
     
        job_list.append(job)
       # print("job: {}".format(job))
    return job_list

driver = webdriver.Chrome()

if __name__ == "__main__":

    categories = ["python","dot-net"]

    skills = Counter() #set()#[]

    try:
        category = "java"
        jobs = work(category)

        for job in jobs:
            job_skills = job['skills']
            skills.update(job_skills)

        print("total {} jobs".format(len(jobs)))
    except Exception as ex:
        print(ex)
    finally:
        driver.close()

    print(skills)