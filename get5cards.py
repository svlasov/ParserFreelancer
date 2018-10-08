import datetime

import requests
from random import choice
from get5cards_find_works import find_works
from time import sleep
from random import uniform


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
		print('Сегодня уже был запрос по прокси')
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

	#print(proxy_list)
	return proxy_list

#'Запрашивает данные с указанного сайта, притворяясь человеком'
def get_html(url, proxy = None, useragent = None):
	'запрашивает страницу притворяясь человеком'
	print('вход в гет штмл')
	r = requests.get(url, proxies = proxy) # headers = useragent,

	#with open('html.txt','w',encoding = 'utf-8') as f:
		#f.write(str(r.text))

	print('притворился')
	return r.text


def get_5_cards(link):
	print('Запуск')
	#url = 'https://www.freelancer.com/jobs/software-architecture/' #!!Это пока заглушка для запроса от бота!!
	url = link
	useragents = open('useragents.txt').read().split('\n')
	proxies = get_proxy()

	while True: #Повторяй цикл до ответа от прокси сервера
		sleep(uniform(3,6))
		proxy = {'http':'http://'+ choice(proxies)}
		useragent = {'User-Agent': choice(useragents)}
		try:
			html = get_html(url,proxy) #useragent,proxy)	#'запрашивает страницу притворяясь человеком'
			break
		except requests.exceptions.RequestException as e:
			#print(e)
			print('________________')

	print('Передаем стр в парсер')
	cards = find_works(html)
		
	#with open('text.txt','w',encoding = 'utf-8') as f:
		#f.write(html)
	#print (cards)
	return cards

if __name__ == '__main__':
	get_5_cards()