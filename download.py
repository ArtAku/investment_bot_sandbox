import os
from tinkoff.invest import Client,InstrumentStatus,exceptions
from datetime import datetime
import json
from time import sleep

CONTRACT_PREFIX = "tinkoff.public.invest.api.contract.v1."
TOKEN =  #os.environ["INVEST_TOKEN"]
INTERVALS = {

}

def convertCandle(candle):
    # open, close, high, low, volume
    return f'{candle.open.units}.{candle.open.nano}|{candle.close.units}.{candle.close.nano}|{candle.high.units}.{candle.high.nano}|{candle.low.units}.{candle.low.nano}|{candle.volume}'

def downloadYear(client, instrument):
    to_ = datetime.now()
    from_ = to_.replace(year=2021)
    figi = instrument.figi
    try:
        res = client.market_data.get_candles(figi=figi,interval=5,from_=from_,to=to_)
    except exceptions.RequestError as ex:
        print('Awaiting')
        sleep(61)
        res = client.market_data.get_candles(figi=figi,interval=5,from_=from_,to=to_)
    cwd = os.getcwd()
    # dir = os.path.join(cwd, "data", figi)
    # if not os.path.exists(dir):
    #     os.mkdir(dir)
    data = []
    for r in res.candles:
        data.append(r.time.strftime("%Y-%m-%d")+ '|' + convertCandle(r)+ f'|{instrument.country_of_risk}|{instrument.currency}')
    with open(os.path.join(cwd, "data",figi + ".txt"),'w') as f:
        f.writelines(data)


def TestDownload():
    with Client(TOKEN) as client:
        # client.market_data.get_candles()
        res = client.instruments.shares(instrument_status=2)
        instruments = res.instruments
        names = {}
        for i in instruments:
            names[i.figi] = i.name

        with open("names.txt",'w') as f:
            f.write(json.dumps(names))

        for instrument in instruments:
            downloadYear(client, instrument)

if __name__ == "__main__":
    TestDownload()
