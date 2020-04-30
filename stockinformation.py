import datetime
from pandas_datareader import data as pdr
import yfinance as yf


class Stockinformation:

    # def __init__(self):
    #     # self.symbol = symbol
    def get_stock_price(self, symbol):
        # yf.pdr_override()
        try:
            stock = pdr.get_data_yahoo(symbol,  start="2020-04-20",
                                       end=datetime.date.today())
            price = (stock["Close"][0]).round(3)
            price = str(price)
            return price
        except KeyError:
            return 'wrong symbol or no actual price'
        except Exception as e:
            print(e)
            return 'No Symbol'
