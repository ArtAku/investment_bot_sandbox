from download import downloadAll
from config import args
from time import sleep
import logging

def loop():
    try:
        while True:
            logging.debug('loop')    
            sleep(1)
    except KeyboardInterrupt:
        logging.info('Program manually stopped')

def main():
    logging.info('Start')
    # loop()
    if args.download:
        downloadAll()

if __name__ == '__main__':
    main()