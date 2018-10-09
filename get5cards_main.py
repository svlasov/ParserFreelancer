"""
Запрашиваем у skillbase.db ссылку на указанный юзером навык
Получаем 5 словарей с данными 5-ти первых карточек на странице
Пока принтим их в консоль в человекочитаемом виде
"""

import sqlalchemy

from skilllist_sql import db_session, Skillbase

from get5cards import get_5_cards


u = Skillbase

while True:
	user_input = input('Укажите навык по которому искать заказы:\n')
	try:
		q = u.query.filter(Skillbase.skill == user_input).first()
		link = q.link
		print(link)
		break
	except AttributeError:
		print('Такого навыка в базе нет')
		user_input = "%" + user_input + "%"
		q_user = u.query.filter(Skillbase.skill_words.like(user_input)).all()
		print("Может быть вы имели ввиду:\n")
		for skil in q_user:
			print(skil.skill)

cards = get_5_cards(link)
for card in cards:
	if card['verified'] == True:
		pay_metod = '\tСпособ оплаты подтвержден'
	else: 
		pay_metod = ''
	print('\nЗадание: {0}\nОплата:{5}{6}\tАктивно еще {1}.\n\nОписание: {2}\n\nТребуемые навыки{3}\n\nПредложений от фрилансеров:{7}\n\nСтраница заказа:  {4}\n\n'.format(card['title'],card['time'],card['description'],card['list_skill'],card['link'],card['price'],pay_metod,card['bids']))