
from tinkoff.invest import Client,exceptions,Share,services
from config import TOKEN


        
def getLatest():


def getLatestAll(client):


def updateData():
    with Client(TOKEN) as client:
        getLatestAll(client)