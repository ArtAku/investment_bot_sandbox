import argparse

CONTRACT_PREFIX = "tinkoff.public.invest.api.contract.v1."
with open('.env','r') as f:
    lines = f.readlines()
ENVS = { l.split('=')[0] : l.split('=')[1] for l in lines }

INTERVALS = {

}


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')

args = parser.parse_args()


