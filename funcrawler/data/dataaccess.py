import mysql.connector
class DataAccess(object):

    @staticmethod
    def get_connection_local():
        return mysql.connector.connect(user='root',password='', host='127.0.0.1', database='fourlols')
    @staticmethod
    def get_connection_prod():
        return mysql.connector.connect(user='n4dlol1_wp',password='AHqypnG&yzue', host='4dlols.com',
                                       database='n4dlol1_wp')
