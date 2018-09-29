import logging

from telegram.ext import Updater, CommandHandler , MessageHandler, RegexHandler, Filters 
from settings import API_KEY 

def hello(bot, update, user_data):
    text = 'Hello!'
    
    update.message.reply_text(text)


def start_bot():
    mybot = Updater(API_KEY)#(API_KEY)
    mydisp = mybot.dispatcher

    # common command handler
    mydisp.add_handler(CommandHandler(["start", "hello"], hello, pass_user_data=True))
    
    mybot.start_polling()
    mybot.idle()

if __name__== '__main__':
    logging.basicConfig(format='%(asctime)s - [%(name)s] - %(levelname)s - %(message)s',
                    level=logging.DEBUG,
                    filename='bot.log')
    telegram_logger = logging.getLogger("telegram")
    telegram_logger.setLevel(logging.INFO)

    print(API_KEY)

    start_bot()  