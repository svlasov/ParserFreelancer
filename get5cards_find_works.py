from bs4 import BeautifulSoup
import re
from get5cards_sql import db_session, Workbase


def find_works(html):#получаем ссылку, число работ
	#bonus = ['local=true','&','fixed=true','fixed_min=','fixed_max=','contest=true','contest_min=','contest_max=','hourly=true','languages=','hourly_duration=']#1-6
	cards = []
	link = {}
	skill_tags = []
	card_list = []
	x=0
	
	#html = open(html).read()
	soup = BeautifulSoup(html,'lxml')
	#Находим лист проектов
	text_block1 = soup.find('div', id= "project-list", class_="JobSearchCard-list")
	#Находим карточки проектов
	text_block1 = text_block1.find_all('div', class_= "JobSearchCard-item-inner")
	#Драим по каждой карточке------------------------------
	for block in text_block1:
		#print(block)
		#Находим название карточки
		title = block.find('a', class_='JobSearchCard-primary-heading-link').contents[0]#,href = re.compile(regexp))
		title = title.replace('  ','')
		title = title.replace('\n','')
		print(title)

		#Заявлено времени назад
		time = block.find('span', class_='JobSearchCard-primary-heading-Days').contents[0]
		time = time.split(' ')
		time.remove('left')
		#print(time)

		#Описание
		description = block.find('p', class_='JobSearchCard-primary-description').contents[0]
		description= description.replace('  ','')
		description = description.replace('\n','')
		#print(description)

		#Список навыков
		skills_block = block.find('div', class_='JobSearchCard-primary-tags')
		skills = skills_block.find_all('a')
		for skill in skills:
			skill = str(skill)
			skill = skill.split('/">')[-1]
			skill = skill.replace('</a>','')
			skill_tags.append(skill)
		list_skill = skill_tags
		skill_tags = []
		#print(list_skill)

		featured = block.find('div', class_="JobSearchCard-primary-promotion")
		featured= 'Featured' in str(featured)
		#print(featured)

		if featured == False:
			#Цена работы
			price_block = block.find('div', class_="JobSearchCard-secondary-price").contents[0]
			price= price_block.replace('  ','')
			price = price.replace('\n','')
			price = price.replace('/ hr','per hour')
			#print(price)

			#Ссылка на работу
			contest = block.find('span', class_="Icon JobSearchCard-primary-heading-Icon")
			contest = 'flicon-trophy' in str(contest)
			if contest:
				regexp= r'^/contest/'
			else:
				regexp= r'^/projects/'

			link_block = block.find('a',href = re.compile(regexp))
			link = link_block.get('href')
			link = 'https://www.freelancer.com' + link
			#print(link)

			#Количество заявок
			bids = block.find('div', class_='JobSearchCard-secondary-entry').contents[0]
			bids = bids.split(' ')[0]
			#print(bids)

		#Верифицировано или нет
		verified = block.find('div', class_="JobSearchCard-primary-heading-status Tooltip--top")
		verified = 'VERIFIED' in str(verified)
		#print(verified)

		#print('---------------')
		if featured == True:
			price = '0'
			link = 'Error 404'
			bids = '0'
		
		card = {'title':title, 'time':time, 'description':description, 'list_skill':list_skill, 'link':link, 'price':price, 'verified':verified, 'bids':bids}
		#print(card)
		cards.append(card)
		x+=1
		if x == 5:
			return cards
	return cards

if __name__ == '__main__':
	find_works()