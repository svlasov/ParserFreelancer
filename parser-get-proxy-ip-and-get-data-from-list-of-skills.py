import requests
from random import choice
#from time import sleep
from random import uniform
from ast import literal_eval as le
from bs4 import BeautifulSoup
import re
import datetime

def get_proxy():
#Мы будем использовать этот код, когда будем запрашивать лист прокси с сайта
	#Загружаем файл	и делаем из него словарь с датой создания на конце
	proxy_list = []
	date_this_request = datetime.datetime.now()
	date_this_request = str(date_this_request).split(' ')[0]			#Мы получили дату

	proxies_list = open('proxies.txt').read()			#Читаем данные из файла в строку

	proxies_list = proxies_list.replace("['",'')
	proxies_list = proxies_list.replace("']",'')
	proxies_list = proxies_list.split("', '")

	if proxies_list[-1] == date_this_request:
		print('Сегодня уже был запрос')
		#Используем список
		del proxies_list[-1]
		x=0
		for key in proxies_list:
			proxy_site = proxies_list[x]
			proxy_list.append(proxy_site)
			x+=1
	else:
		#Запрашиваем новый список прoкси
		result = requests.get('https://htmlweb.ru/geo/api.php?proxy&short&json')
		if result.status_code == 200:
			result = result.json()
			del result['limit']			#Удаляем лишнее значение
			x=0
			for key in result:
				x= str(x)
				proxy_site = result[x]
				proxy_list.append(proxy_site)
				x= int(x)
				x+=1
			proxy_list_for_save = proxy_list
			proxy_list_for_save.append(str(date_this_request))			#Добавляем дату
			proxy_list_for_save = str(proxy_list_for_save)			#превращаем словарь в строку
			print ('Получен новый список прокси')
			with open('proxies.txt','w',encoding = 'utf-8') as f:
				f.write(proxy_list_for_save)
		else:
			print("Мы не получили новый прокси лист, используем старый.")
			del proxies_list['date']
			x=0
			for key in proxies_list:
				proxy_site = proxies_list[x]
				proxy_list.append(proxy_site)
				x+=1

	print(proxy_list)
	return proxy_list

#'Запрашивает данные с указанного сайта, притворяясь человеком'
def get_html(url, useragent = None, proxy = None):
	'запрашивает страницу притворяясь человеком'
	print('вход в гет штмл')
	r = requests.get(url, headers = useragent, proxies = proxy)
	print('притворился')
	return r.text

#парсим https://www.freelancer.com/job/
def find_links(html):
	print('вход в финд линкс')
	skill_words = []
	works = []
	regexp= r'^/jobs/'
	regexp2= r'\(\b\d\b\)'
	soup = BeautifulSoup(html,'lxml')
	#Находим блок "Websites, IT & Software"
	text_block1 = soup.find('ul', class_ = "PageJob-browse-list Grid")
	#print(text_block1)
	text_block3 = text_block1.find_all('a', class_="PageJob-category-link ", href = re.compile(regexp))
	#print(text_block3)

	for block in text_block3:
		#print(block)
		link = block.get('href')
		link = 'https://www.freelancer.com' + link
		#print(link)
		str2 = block.get('title')
		title_str = re.sub(r' Jobs','',str2)
		#print(title_str)
		str3 = block.contents[0]
		str3 = re.sub(r'  ','',str3)
		str3 = re.sub(r'\n','',str3)
		str3 = str3.split('\xa0')
		work_count = (re.search(r'\d+', str(str3[-1].strip()))).group()
		#print(work_count)
		skill_words = title_str.replace('(','')
		skill_words = skill_words.replace(')','')
		skill_words = skill_words.replace('.','')
		skill_words = skill_words.replace(' / ',' ')
		skill_words = skill_words.replace('/',' ')
		skill_words = skill_words.replace(' for ',' ')
		skill_words = skill_words.replace(' on ',' ')
		skill_words = skill_words.lower()
		skill_words = skill_words.split(' ')
		if ' ' in skill_words:
			skill_words = skill_words.remove(' ')
		if len(skill_words)>1:
			skill_words.append((title_str).lower())
		#print(skill_words)
		
		skill = {'skill':title_str, 'link':link, 'work_count':work_count,'skill_words':skill_words}
		#print(skill)
		works.append(skill)
	return(works)


def main():
	print('Запуск')
	url = 'https://www.freelancer.com/job/'
	useragents = open('useragents.txt').read().split('\n')
	proxies = get_proxy()	#open('proxies.txt').read().split('\n')

	while True: #Повторяй цикл до ответа от прокси сервера
		#sleep(uniform(1,2))
		proxy = {'http':'http://'+ choice(proxies)}
		useragent = {'User-Agent': choice(useragents)}
		try:
			html = get_html(url,proxy)#,useragent,proxy)	#'запрашивает страницу притворяясь человеком'
			break
		except Exception:
			print('Слишком медленный прокси')


	#with open('text.txt','w',encoding = 'utf-8') as f:
		#f.write(html)
	works_list = find_links(html)
		
	#with open('text.txt','w',encoding = 'utf-8') as f:
		#f.write(html)
	print('взяли страницу')
	

	print(works_list)			#Позже здесь будет жить return works_list

if __name__ == '__main__':
	main()