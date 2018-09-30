#'Запрашивает данные с указанного сайта, притворяясь человеком'
import requests
from bs4 import BeautifulSoup
from random import choice
from time import sleep
from random import uniform


def get_proxy():
	'Получает список прокси'
	proxy_list = []
	result = requests.get('https://htmlweb.ru/geo/api.php?proxy&short&json')
	if result.status_code == 200:
		data = result.json()
		for i in range(50):
			proxy_list.append(str(data[str(i)]))
		print ('Получен список прокси')
		return proxy_list
	else:
		print("Мы не получили прокси лист")



def get_html(url, useragent = None, proxy = None):
	'запрашивает страницу притворяясь человеком'
	print('вход в гет штмл')
	r = requests.get(url,headers = useragent, proxies = proxy)
	return r.text


def get_ip(html):
	print('вход в гет ай пи')
	soup = BeautifulSoup(html,'lxml')
	ip = soup.find('span',class_ = 'ip').text.strip()
	ua = soup.find('span',class_ = 'ip').find_next_sibling('span').text.strip()
	print(ip)
	print(ua)
	print('----------------')


def main():
	url = 'http://sitespy.ru/my-ip'
	useragents = open('useragents.txt').read().split('\n')
	proxies = get_proxy()
	for i in range (10):
		print(i)
		sleep(uniform(1,2))
		proxy = {'http':'http://'+ choice(proxies)}
		useragent = {'User-Agent': choice(useragents)}

		try:
			html = get_html(url,useragent,proxy)
		except:
			print('oops - Вероятно прокси сервер {} не дал ответа'.format(proxy))
			continue
		try:
			get_ip(html)
		except:
			print('oops - Вероятно нас приняли за робота -_-"')
			print(useragent)
			print(proxy)
			continue
if __name__ == '__main__':
	main()