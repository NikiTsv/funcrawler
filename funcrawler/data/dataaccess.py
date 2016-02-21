import mysql.connector
class DataAccess(object):

    @staticmethod
    def get_connection():
        return mysql.connector.connect(user='root',password='', host='127.0.0.1', database='fourlols')