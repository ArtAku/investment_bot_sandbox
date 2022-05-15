from time import sleep
from config import TIMEOUT,REALEXCHANGE
from tinkoff.invest import exceptions
import logging
from tinkoff.invest.services import HistoricCandle
from tinkoff.invest import Share,Quotation
import json

def safeRequest(f,args):
    try:
        res = f(**args)
    except exceptions.RequestError as ex:
        logging.warning('Limit reached, awaiting')
        sleep(TIMEOUT)
        res = f(**args)
    return res

class stringify():
    """
    svc scheme
    open;clos;high;low;volume;
    """
    def covnertCandle(candle:HistoricCandle)->str:
        # open, close, high, low, volume
        return f'{candle.open.units}.{candle.open.nano};{candle.close.units}.{candle.close.nano};{candle.high.units}.{candle.high.nano};{candle.low.units}.{candle.low.nano};{candle.volume}'

    """
    json scheme
    {
        "figi":{
            "name":str
            "figi":str
            "lot":str
            "currency":str
            "klong":str
            "kshort":str
            "exchange":str
            "country_of_risk":str
            "otc_flag":str
            "real_exchange":str
        }
    }
    """
    def convertShare(share:Share, returnStr:bool = True)->dict[str, dict[str,str]] or str :
        data = {
            "name":share.name,
            "figi":share.figi,
            "lot":str(share.lot),
            "currency":share.currency,
            "klong":stringify.convertQuotation(share.klong),
            "kshort":stringify.convertQuotation(share.kshort),
            "exchange":share.exchange,
            "country_of_risk":share.country_of_risk,
            "otc_flag":str(share.otc_flag),
            "real_exchange": stringify.convertEchange(share.real_exchange.real)
        }
        if returnStr:
            json.dumps(data)
        else:
            return data

    def convertQuotation(quotation:Quotation)->str:
        return f'{quotation.units}.{quotation.nano}'

    def convertEchange(real_exchange:int)->str:
        return REALEXCHANGE[real_exchange]
