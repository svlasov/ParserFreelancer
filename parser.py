#Получает со страницы фрилансера словари{
#'skill':название скилла,
#'link':ссылка на перечень,
#'work_count':число заказов,
#'skill_words':ключевые слова}  

#import request
from bs4 import BeautifulSoup
import re

#def get_html(url):
	#r = request.get(url)
	#return r.text

#get_html(https://www.freelancer.com/job/)

#soup = BeautifulSoup(html,'lxml')

def find_links():
	#парсим https://www.freelancer.com/job/
	#link = {}
	skill_words = []
	works = []

	regexp= r'^https://www.freelancer.com/jobs/'
	regexp2= r'\(\b\d\b\)'
	html = open('Freelance Jobs and Projects _ Freelancer.html').read()
	soup = BeautifulSoup(html,'lxml')
	#Находим блок "Websites, IT & Software"
	text_block1 = soup.find('ul', class_ = "PageJob-browse-list Grid")
	text_block3 = text_block1.find_all('a',href = re.compile(regexp))
	
	for block in text_block3:
		link = block.get('href')
		str2 = block.get('title')
		title_str = re.sub(r' Jobs','',str2)
		
		str3 = (block.contents)[0]
		str3 = re.sub(r'  ','',str3)
		str3 = re.sub(r'\n','',str3)
		str3 = str3.split('\xa0')
		work_count = (re.search(r'\d+', str(str3[-1].strip()))).group()
		
		skill_words = title_str.replace('(','')
		skill_words = skill_words.replace(')','')
		skill_words = skill_words.replace('.','')
		skill_words = skill_words.replace(' / ',' ')
		skill_words = skill_words.replace('/',' ')
		skill_words = skill_words.replace(' for ',' ')
		skill_words = skill_words.replace(' on ',' ')
		skill_words = skill_words.split(' ')
		if ' ' in skill_words:
			skill_words = skill_words.remove(' ')
		if len(skill_words)>1:
			skill_words.append(title_str)
		
		skill = {'skill':title_str, 'link':link, 'work_count':work_count,'skill_words':skill_words}
		print(skill)
		works.append(skill)
	#return(works)
	
if __name__ == '__main__':
	find_links()