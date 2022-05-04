from os.path import join
from tinkoff.invest import Client,exceptions,Share,services
from datetime import datetime,timezone
import json
from config import cwd, ENVS, INTERVALS, INSTRUMENTS
from supply import safeRequest
import logging

TOKEN = ENVS['TOKEN_READ']

def convertCandle(candle):
    # open, close, high, low, volume
    return f'{candle.open.units}.{candle.open.nano};{candle.close.units}.{candle.close.nano};{candle.high.units}.{candle.high.nano};{candle.low.units}.{candle.low.nano};{candle.volume}'

def downloadYears(client:services, instrument:Share):
    logging.debug(f'{instrument.name}')
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
        res = safeRequest(client.market_data.get_candles, {"figi":figi,"interval":INTERVALS['CANDLE_INTERVAL_DAY'],"from_":from_,"to":to_})
        if not len(res.candles):
            return
        for r in res.candles[::-1]:
            data.append(r.time.strftime("%Y-%m-%d")+ ';' + convertCandle(r)+ f';{instrument.country_of_risk};{instrument.currency}\n')
    with open(join(cwd, "data", figi + ".csv"),'w') as f:
        f.writelines(data)

def downloadAll():
    with Client(TOKEN) as client:
        instruments = updateInfo()
        for instrument in instruments:
            downloadYears(client, instrument)

def updateInfo():
    with Client(TOKEN) as client:
        res = safeRequest(client.instruments.shares,{"instrument_status":INSTRUMENTS['INSTRUMENT_STATUS_ALL']})
        names = {}
        for i in res.instruments:
            names[i.figi] = i.name

        with open(join(cwd,"data","info.json"),'w') as f:
            f.write(json.dumps(names))
        return res.instruments
