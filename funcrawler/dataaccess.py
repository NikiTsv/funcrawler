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
        # Insert new
        cursor.execute(add_post, (data.title, data.content, data.contentType, data.contentUrl, data.points, today))
        emp_no = cursor.lastrowid

        # Make sure data is committed to the database
        cnx.commit()
        cursor.close()
        cnx.close()

    def insert_posts(self, post_data):
        cnx = self.__get_connection()
        cursor = cnx.cursor()
        today = datetime.now()
        add_post_query = self.__get_add_post_query()

        for data in post_data:
            # Insert new
            cursor.execute(add_post_query, (data.title, data.content, data.contentType, data.contentUrl, data.points, today))
            #emp_no = cursor.lastrowid  #scope_identity
       
        # Make sure data is committed to the database
        cnx.commit()
        cursor.close()
        cnx.close()            

    def __get_connection(self):
        return mysql.connector.connect(user='root',password='', host='127.0.0.1', database='fourlols')
    
    def __get_add_post_query(self):
        return ("INSERT INTO post "
                       "(title, content, contentUrl, ContentType, Points, DateCreated) "
                       "VALUES (%s, %s, %s, %s, %s, %s)")
    

