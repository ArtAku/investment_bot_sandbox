from datetime import datetime
from time import sleep
from foreteller import foreteller
from tinkoff.invest import HistoricCandle, OrderBook, Trade
from trader import trader
from storage import Storage
from config import INTERVALS

class tester():

    _foreteller:foreteller
    _trader:trader
    _database:Storage
    interval:int

    deposit:float
    maxSell:float
    maxBuy:float

    def __init__(self, host:str, user:str, password:str, TEST_CONFIG) -> None:
        self._foreteller = foreteller()
        self._trader = trader()
        self._database = Storage(host, user, password)
        self.interval = INTERVALS[TEST_CONFIG['interval']]
        self.deposit = TEST_CONFIG['limits']['deposit']
        self.maxSell = TEST_CONFIG['limits']['sell']
        self.maxBuy = TEST_CONFIG['limits']['buy']

    def getData(self) -> tuple[list[HistoricCandle],list[OrderBook],list[Trade]]:
        pass

    def tick(self):
        data = self.getData()
        candle = self._foreteller.foretellCandle(data[0], self.interval)
        orders = self._foreteller.foretellOrders(data[1], data[2])
        actions = self._trader.guess(candle, orders)
        self._database.put(actions, datetime.now())
