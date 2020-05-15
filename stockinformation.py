from datetime import datetime, timedelta
from pandas_datareader import data as pdr
import yfinance as yf

days_to_subtract = 5


class Stockinformation:

    # def __init__(self):
    #     # self.symbol = symbol
    def get_stock_price(self, symbol):
        # yf.pdr_override()
        try:
            stock = pdr.get_data_yahoo(symbol,  start=datetime.today() - timedelta(days=days_to_subtract),
                                       end=datetime.today())
            price = (stock["Close"][-1]).round(3)
            price = str(price)
            return price
        except KeyError:
            return 'wrong symbol or no actual price'
        except Exception as e:
            print(e)
            return 'No Symbol'
