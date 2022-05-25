import argparse
from os import getcwd
import logging
from environs import Env
import datetime
import yaml

CONTRACT_PREFIX = "tinkoff.public.invest.api.contract.v1."

env = Env()
env.read_env() 

TEST_CONFIG = {}
with open('test.yaml', 'r') as file:
    TEST_CONFIG = yaml.safe_load(file)

TIMEOUT = 61 #seconds

INTERVALS = {
    "CANDLE_INTERVAL_UNSPECIFIED" : 0,
    "CANDLE_INTERVAL_1_MIN" : 1,
    "CANDLE_INTERVAL_5_MIN" : 2,
    "CANDLE_INTERVAL_15_MIN" : 3,
    "CANDLE_INTERVAL_HOUR" : 4,
    "CANDLE_INTERVAL_DAY" : 5
}
INSTRUMENTS = {
    "INSTRUMENT_STATUS_UNSPECIFIED": 0,
    "INSTRUMENT_STATUS_BASE": 1,
    "INSTRUMENT_STATUS_ALL": 2
}
REALEXCHANGE = {
    "REAL_EXCHANGE_UNSPECIFIED": 0,
    "REAL_EXCHANGE_MOEX": 1,
    "REAL_EXCHANGE_RTS": 2,
    "REAL_EXCHANGE_OTC": 3,

    0:"UNSPECIFIED",
    1:"MOEX",
    2:"RTS",
    3:"OTC"
}

def valid_date(s):
    try:
        return datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        msg = "not a valid date: {0!r}".format(s)
        raise argparse.ArgumentTypeError(msg)

parser = argparse.ArgumentParser(description='Trading tinkoff app')
parser.add_argument('--download', dest='download', action='store_const',
                    const=True, default=False,
                    help='download shares data')
parser.add_argument('--timefrom', dest='timefrom', action='store',
                    help='set timerange in YYYY-MM-DDTHH:MM:SS from <timefrom> to now for custom download', type=valid_date)
parser.add_argument('--interval', dest='interval', action='store',
                    choices=["1_MIN","5_MIN","15_MIN","HOUR","DAY"],
                    help='set available intervals for custom download. 1,5,15 min max for 1 day, 1 hour for 1 week and 1 day for 1 year')
parser.add_argument('--mysql', dest='mysql', action='store_const',
                    const=True, default=False,
                    help='enable mysql saving')
parser.add_argument('--logLevel', dest='logLevel', action='store', 
                    default="INFO",
                    choices=["DEBUG","INFO","WARNING","ERROR","CRITICAL"],
                    help='logging level, can be: DEBUG,INFO,WARNING,ERROR,CRITICAL. Default INFO')

args = parser.parse_args()
cwd = getcwd()

def setLogLevel(logLevel):
    logging.basicConfig(level=getattr(logging,logLevel))

setLogLevel(args.logLevel)
