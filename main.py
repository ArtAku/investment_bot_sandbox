from download import downloadAll
from config import args
from time import sleep

def loop():
    try:
        while True:
            print('loop')    
            sleep(1)
    except KeyboardInterrupt:
        print('Program manually stopped')

def main():
    print('Start')
    # loop()
    downloadAll()

if __name__ == '__main__':
    main()