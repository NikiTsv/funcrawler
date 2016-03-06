from data.dataaccess import DataAccess
import mysql.connector
import time
import datetime
from data.dataaccess import DataAccess
from datetime import datetime


class Log(DataAccess):

    def write_error(self, logdata):
        cnx = self.get_connection_local()
        cursor = cnx.cursor()
        today = datetime.now()
        write_log_entry_query = self.__get_write_log_entry_query()
        cursor.execute(write_log_entry_query, ("High", logdata.message, logdata.source, today, "Error"))

        try:
            cnx.commit()
            cursor.close()
            cnx.close()
        except Exception as ex:
            print('An exception occured when commiting transaction! ' + str(ex))
            cursor.close()
            cnx.close()
            raise

    def write_notification(self, logdata):
        cnx = self.get_connection_local()
        cursor = cnx.cursor()
        today = datetime.now()
        write_log_entry_query = self.__get_write_log_entry_query()
        cursor.execute(write_log_entry_query, ("Medium", logdata.message, logdata.source, today, "Notification"))
        try:
            cnx.commit()
            cursor.close()
            cnx.close()
        except Exception as ex:

            print('An exception occured when commiting transaction! ' + str(ex))
            cursor.close()
            cnx.close()
            raise

    def __get_write_log_entry_query(self):
        return ("INSERT INTO log (Level, Message, Source, DateCreated, Type) "
                       "VALUES (%s, %s, %s, %s, %s)")