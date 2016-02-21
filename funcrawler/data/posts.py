import mysql.connector
import time
import datetime
from data.dataaccess import DataAccess
from datetime import datetime


class Posts(DataAccess):
    """description of class"""

    def insert_posts(self, post_data):
        cnx = self.get_connection()
        cursor = cnx.cursor()
        today = datetime.now()
        add_post_query = self.__get_add_post_query()
        check_query = self.__get_check_if_post_exists_query()
        successful_writes = 0
        for data in post_data:
           try:
             cursor.execute(check_query, ({'contentUrl': data.contentUrl}))
             if not cursor.fetchone()[0]:
                cursor.execute(add_post_query, (data.title, data.content, data.contentUrl, data.contentType, data.points, today))
                successful_writes = successful_writes + 1
                print('Row inserted!')
             else:
                 print('Url already exists in the database!')

           except Exception as ex:
                print('An exception occured when writing to database! ' + str(ex))
        try:
            cnx.commit()
            cursor.close()
            cnx.close()
        except Exception as ex:
            print('An exception occured when commiting transaction! ' + str(ex))
            cnx.close()
            raise           
        return successful_writes

    def __get_add_post_query(self):
        return ("INSERT INTO post "
                       "(title, content, contentUrl, ContentType, Points, DateCreated) "
                       "VALUES (%s, %s, %s, %s, %s, %s)")

    def __get_check_if_post_exists_query(self):
        return ("SELECT COUNT(Id) FROM post WHERE contentUrl = %(contentUrl)s")

