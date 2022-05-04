from time import sleep
from config import TIMEOUT
from tinkoff.invest import exceptions
import logging

def safeRequest(f,args):
    try:
        res = f(**args)
    except exceptions.RequestError as ex:
        logging.warning('Limit reached, awaiting')
        sleep(TIMEOUT)
        res = f(**args)
    return res
