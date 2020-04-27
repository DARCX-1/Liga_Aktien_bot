#https://www.codementor.io/@garethdwyer/building-a-telegram-bot-using-python-part-1-goi5fncay
#https://codeburst.io/indian-stock-market-price-notifier-bot-telegram-92e376b0c33a


from functions import DBHelper
from functions import bot
import time

db = DBHelper()
bot_name='stocks_bot'
token_directory='../Token/Token_Liga_bot.txt'
bot = bot(token_directory)



def main():
    db.setup()
    last_update_id = None
    while True:
        print("getting updates")
        updates = bot.get_updates(last_update_id)
        print(updates)
        if len(updates["result"]) > 0:
            last_update_id = bot.get_last_update_id(updates) + 1
            bot.decide(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()

