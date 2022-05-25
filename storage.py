from datetime import datetime
from mysql.connector import connect, Error
import logging


class Storage():
    connection = ''

    def __init__(self,host,user,password) -> None:
        try:
            self.connection = connect(host,user,password,)
        except Error as e:
            logging.error(e)
    
    def put(self, actions:dict[str,tuple[int,float]], t:datetime) -> bool:
        pass