from download import downloader
from config import args, env, TEST_CONFIG
from time import sleep
import logging
from test import tester

def loop():
    try:
        while True:
            logging.debug('loop')    
            sleep(1)
    except KeyboardInterrupt:
        logging.info('Program manually stopped')

def main():
    logging.info('Start')
    if args.download:
        d = downloader()
        if args.timefrom or args.interval:
            d.downloadAll(True, args.timefrom, args.interval)
        else:
            d.downloadAll()
    else:
        loop()

def test(steps:int):
    logging.info('Testing')
    t = tester(env('MYSQL_HOST'), env('MYSQL_USER'), env('MYSQL_PASS'), TEST_CONFIG)
    for i in range(steps):
        t.tick()

if __name__ == '__main__':
    main()
