from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def work():

    url = "https://www.freelancer.com/jobs/dot-net/"

    driver.get(url)

    # elem = driver.find_element_by_id("project-list")
    job_elems = driver.find_elements_by_css_selector("#project-list .JobSearchCard-item-inner")

    for job_elem in job_elems:
        # title = block.find('a', class_='JobSearchCard-primary-heading-link').contents[0]

        job = {}

        title_elem = job_elem.find_element_by_css_selector("a.JobSearchCard-primary-heading-link")
        job['title'] = title_elem.text
        job['url'] = title_elem.get_attribute("href")

        days_ago_elem = job_elem.find_element_by_css_selector("span.JobSearchCard-primary-heading-Days")
        job['days_ago'] = days_ago_elem.text

        # description = block.find('p', class_='JobSearchCard-primary-description').contents[0]
        description_elem = job_elem.find_element_by_css_selector("p.JobSearchCard-primary-description")
        job['description'] = description_elem.text

        # skills_block = block.find('div', class_='JobSearchCard-primary-tags')
		# skills = skills_block.find_all('a')
        skill_elems = job_elem.find_elements_by_css_selector("div.JobSearchCard-primary-tags a")
        job['skills'] = [se.text for se in skill_elems]

        print("job: {}".format(job))

driver = webdriver.Chrome()
try:
    work()
except Exception as ex:
    print(ex)
finally:
    driver.close()