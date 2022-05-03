from os.path import join
from tinkoff.invest import Client,exceptions,Share,services
from datetime import datetime,timezone
import json
from time import sleep
from config import cwd, ENVS, INTERVALS, INSTRUMENTS

TOKEN = ENVS['TOKEN_READ']

def convertCandle(candle):
    # open, close, high, low, volume
    return f'{candle.open.units}.{candle.open.nano};{candle.close.units}.{candle.close.nano};{candle.high.units}.{candle.high.nano};{candle.low.units}.{candle.low.nano};{candle.volume}'

def downloadYears(client:services, instrument:Share):
    print(f'{instrument.name}')
    now = datetime.now(timezone.utc)
    to_ = datetime.now(timezone.utc)
    from_ = to_.replace(year=to_.year-1)
    figi = instrument.figi
    if instrument.ipo_date > from_:
        return
    years = (to_ - instrument.ipo_date).days // 365
    data = ['time;open;close;high;low;volume;country;currency\n']
    for y in range(years):
        to_ = now.replace(year=now.year-y)
        from_ = now.replace(year=now.year-1-y)
        try:
            res = client.market_data.get_candles(figi=figi,interval=INTERVALS['CANDLE_INTERVAL_DAY'],from_=from_,to=to_)
        except exceptions.RequestError as ex:
            print('Awaiting')
            sleep(61)
            res = client.market_data.get_candles(figi=figi,interval=INTERVALS['CANDLE_INTERVAL_DAY'],from_=from_,to=to_)
        if not len(res.candles):
            return
        for r in res.candles[::-1]:
            data.append(r.time.strftime("%Y-%m-%d")+ ';' + convertCandle(r)+ f';{instrument.country_of_risk};{instrument.currency}\n')
    with open(join(cwd, "data", figi + ".csv"),'w') as f:
        f.writelines(data)

def downloadAll():
    with Client(TOKEN) as client:
        res = client.instruments.shares(instrument_status=INSTRUMENTS['INSTRUMENT_STATUS_ALL'])
        instruments = res.instruments
        names = {}
        for i in instruments:
            names[i.figi] = i.name

        with open(join(cwd,"data","names.json"),'w') as f:
            f.write(json.dumps(names))

        for instrument in instruments:
            downloadYears(client, instrument)

