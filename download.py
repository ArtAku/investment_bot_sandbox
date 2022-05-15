from os.path import join
from tinkoff.invest import Client,exceptions,Share,services
from datetime import datetime,timezone
import json
from config import cwd, ENVS, INTERVALS, INSTRUMENTS
from supply import safeRequest,stringify
import logging
import datetime


class downloader():

    intervals = {
        "UNSPECIFIED":  {"id":0, "delta":datetime.timedelta(seconds=0)},
        "1_MIN" :       {"id":1, "delta":datetime.timedelta(minutes=1) , "limit":datetime.timedelta(days=1)  },
        "5_MIN" :       {"id":2, "delta":datetime.timedelta(minutes=5) , "limit":datetime.timedelta(days=1)  },
        "15_MIN" :      {"id":3, "delta":datetime.timedelta(minutes=15), "limit":datetime.timedelta(days=1)  },
        "HOUR" :        {"id":4, "delta":datetime.timedelta(hours=1)   , "limit":datetime.timedelta(weeks=1) },
        "DAY" :         {"id":5, "delta":datetime.timedelta(days=1)    , "limit":datetime.timedelta(days=365)}
    }


    """
    Download shares with lifetime more than year with interval day
    """
    def downloadYears(self, client:services, instrument:Share):
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
            res = safeRequest(client.market_data.get_candles, {"figi":figi,"interval":self.intervals['DAY']['delta'],"from_":from_,"to":to_})
            if not len(res.candles):
                return
            for r in res.candles[::-1]:
                data.append(r.time.strftime("%Y-%m-%d")+ ';' + stringify.convertCandle(r)+ f';{instrument.country_of_risk};{instrument.currency}\n')
        with open(join(cwd, "data", figi + ".csv"),'w') as f:
            f.writelines(data)

    """
    Download shares historic data for custom range with interval specified
    """
    def downloadCustom(self, client:services, instrument:Share, timerange:datetime.timedelta, interval:str):
        
        limit = self.intervals[interval]['limit']
        id = self.intervals[interval]['id']

        logging.debug(f'{instrument.name}')
        to_ = datetime.now(timezone.utc)
        from_ = to_ - timerange
        figi = instrument.figi
        if instrument.ipo_date < from_:
            logging.warn(f'{instrument.name} have not enought historic data for timerange {timerange}')
            return
        
        data = ['time;open;close;high;low;volume;country;currency\n']
        intervals = (to_ - instrument.ipo_date) // limit
        for i in range(intervals):
            to_interval = from_ + limit * (i + 1)
            from_interval = from_ + limit * i
            res = safeRequest(client.market_data.get_candles, {"figi":figi,"interval":id,"from_":from_interval,"to":to_interval})
            if not len(res.candles):
                return
            for r in res.candles[::-1]:
                data.append(r.time.strftime("%Y-%m-%d")+ ';' + stringify.convertCandle(r)+ f';{instrument.country_of_risk};{instrument.currency}\n')
        with open(join(cwd, "data", figi + ".csv"),'w') as f:
            f.writelines(data)

    def downloadAll(self, is_custom=False, timefrom:datetime.datetime=None, interval:str=None):
        with Client(ENVS['TOKEN_READ']) as client:
            instruments = self.updateInfo()

            n = datetime.datetime.now()
            time = self._calcDownloadTime(instruments, timefrom, interval, n)
            logging.info(f'Downloading take about {str(time)}')

            if is_custom:
                if n < timefrom:
                    raise Exception("Timerange later than now")
                for instrument in instruments:
                    self.downloadCustom(client, instrument, n - timefrom,interval)
            else:
                for instrument in instruments:
                    self.downloadYears(client, instrument)

    def _calcDownloadTime(self, instruments:list[Share], timefrom:datetime.datetime=None, interval:str=None, n:datetime.datetime=datetime.datetime.now())->datetime.timedelta:
        requests = 0
        limit = self.intervals[interval]['limit']
        for i in instruments:
            f = max(timefrom, i.ipo_date.replace(tzinfo=None))
            requests += ((n - f) // limit) + 1
        return datetime.timedelta(minutes=(requests/100))

    def updateInfo(self):
        with Client(ENVS['TOKEN_READ']) as client:
            res = safeRequest(client.instruments.shares,{"instrument_status":INSTRUMENTS['INSTRUMENT_STATUS_ALL']})
            logging.info(f'{len(res.instruments)} shares found')
            info = {}
            for i in res.instruments:
                info[i.figi] = stringify.convertShare(i,False)

            with open(join(cwd,"data","info.json"),'w') as f:
                f.write(json.dumps(info))
        return res.instruments
