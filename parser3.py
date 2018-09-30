from bs4 import BeautifulSoup
import re

def find_works():#получаем ссылку, число работ
	link = {}
	skill_tags = []
	card_list = []
	#x=0
	regexp= r'^https://www.freelancer.com/projects/'
	html = open('_NET Jobs.html').read()
	soup = BeautifulSoup(html,'lxml')
	#Находим лист проектов
	text_block1 = soup.find('div', id= "project-list", class_="JobSearchCard-list")
	#Находим карточки проектов
	text_block1 = text_block1.find_all('div', class_= "JobSearchCard-item-inner")
	#Драим по каждой карточке------------------------------
	for block in text_block1:
		#x+=1
		#print(x)
		#Находим название карточки
		title = block.find('a', class_='JobSearchCard-primary-heading-link').contents[0]#,href = re.compile(regexp))
		title = title.replace('  ','')
		title = title.replace('\n','')
		#print(title)

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

		#Ссылка на работу
		link_block = block.find('a',href = re.compile(regexp))
		link = link_block.get('href')
		#print(link)

		#Цена работы
		price_block = block.find('div', class_="JobSearchCard-secondary-price").contents[0]
		price= price_block.replace('  ','')
		price = price.replace('\n','')
		price = price.replace('/ hr','per hour')
		#print(price)

		#Верифицировано или нет
		verified = block.find('div', class_="JobSearchCard-primary-heading-status Tooltip--top")
		verified = 'VERIFIED' in str(verified)
		#print(verified)

		#Количество заявок
		bids = block.find('div', class_='JobSearchCard-secondary-entry').contents[0]
		bids = bids.split(' ')[0]
		#print(bids)

		#print('---------------')
		
		card = {'title':title, 'time':time, 'description':description, 'list_skill':list_skill, 'link':link, 'price':price, 'verified':verified, 'bids':bids}
		print(card)
		card_list.append(card)

if __name__ == '__main__':
	find_works()