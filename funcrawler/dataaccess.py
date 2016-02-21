import mysql.connector
import time
import datetime
from datetime import datetime

class dataaccess(object):
    """description of class"""
    """('test','test','test','test',10000,today)"""
    def insert_post(self,data):
        cnx = self.__get_connection()
        cursor = cnx.cursor()
        today = datetime.now().date()

        add_post = self.__get_add_post_query()
      
        cursor.execute(add_post, (data.title, data.content, data.contentType, data.contentUrl, data.points, today))
        emp_no = cursor.lastrowid

        cnx.commit()
        cursor.close()
        cnx.close()

    def insert_posts(self, post_data):
        cnx = self.__get_connection()
        cursor = cnx.cursor()
        today = datetime.now()
        add_post_query = self.__get_add_post_query()
        successful_writes = 0
        for data in post_data:
           try:
            cursor.execute(add_post_query, (data.title, data.content, data.contentType, data.contentUrl, data.points, today))
            successful_writes = successful_writes + 1
           except Exception as ex:
                print('An exception occured when writing to database! ' + ex)
        try:
            cnx.commit()
            cursor.close()
            cnx.close()
        except Exception as ex:
            print('An exception occured when commiting transaction! ' + ex) 
            cnx.close()
            raise           
        return successful_writes
    def __get_connection(self):
        return mysql.connector.connect(user='root',password='', host='127.0.0.1', database='fourlols')
    
    def __get_add_post_query(self):
        return ("INSERT INTO post "
                       "(title, content, contentUrl, ContentType, Points, DateCreated) "
                       "VALUES (%s, %s, %s, %s, %s, %s)")
    

