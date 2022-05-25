from tinkoff.invest import HistoricCandle, OrderBook, Trade
from config import INTERVALS

class foreteller():

    lengthCandles = 2
    lengthOrders = 2

    def foretellCandle(self,candles:list[HistoricCandle], candleInterval: int) -> HistoricCandle:
        pass

    def foretellOrders(self,orders:list[OrderBook], trades:list[Trade]) -> OrderBook:
        pass
