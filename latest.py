from mysql.connector import connect, Error
from tinkoff.invest import Client,exceptions,Share,services
from config import TOKEN
import logging

class Storage():
    connection = ''

    def __init__(self,host,user,password) -> None:
        try:
            self.connection = connect(host,user,password,)
        except Error as e:
            logging.error(e)
        
def getLatest():


def getLatestAll(client):


def updateData():
    with Client(TOKEN) as client:
        getLatestAll(client)