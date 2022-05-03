import argparse
from os import getcwd

CONTRACT_PREFIX = "tinkoff.public.invest.api.contract.v1."
with open('.env','r') as f:
    lines = f.readlines()
ENVS = { l.split('=')[0] : l.split('=')[1] for l in lines }

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

parser = argparse.ArgumentParser(description='Trading tinkoff app')
parser.add_argument('--download', dest='download', action='store_const',
                    const=True, default=False,
                    help='test download')

args = parser.parse_args()

cwd = getcwd()