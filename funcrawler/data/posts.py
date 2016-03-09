import mysql.connector
import time
import datetime
from data.dataaccess import DataAccess
from datetime import datetime
from models.postmodel import PostWpModel

class Posts(DataAccess):
    """local database"""

    def insert_posts(self, post_data):
        cnx = self.get_connection_local()
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
                successful_writes += 1
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


class PostsWp(DataAccess):
    """production database"""
    user_id = 7

    def insert_posts(self, post_data):
        cnx = self.get_connection_prod()
        cursor = cnx.cursor()
        add_post_query = self.__get_add_post_query()
        check_query = self.__get_check_if_post_exists_query()
        successful_writes = 0
        for data in post_data:
           try:
             cursor.execute(check_query, ({'contentUrl': "%" + data.contentUrl + "%"}))
             result = cursor.fetchone()[0]
             if not result:
                wp_post = self.__generate_wp_post(data)
                self.__execute_insert(cursor, add_post_query, wp_post)
                self.__insert_likes(cursor, self.__get_insert_likes_query(), cursor.lastrowid, data.points)
                #cursor.execute(self.__get_update_post_guid_query(), ({'ID': new_post_id})) -- moved in main for all
                successful_writes += 1
                print('Row inserted!')
             else:
                 print('Url ' + data.contentUrl + ' already exists in the database!')

           except Exception as ex:
                print('An exception occured when writing to database! ' + str(ex))
        try:
            cnx.commit()
            cursor.close()
            cnx.close()
        except Exception as ex:
            print('An exception occured when commiting transaction! ' + str(ex))
            cnx.close()
            raise ex
        return successful_writes

    def update_posts_guid(self):
        cnx = self.get_connection_prod()
        cursor = cnx.cursor()
        cursor.execute(self.__get_update_post_guid_query())
        try:
            cnx.commit()
            cursor.close()
            cnx.close()
        except Exception as ex:
            print('An exception occured when updating post guid! ' + str(ex))
            cnx.close()
            raise ex

    def __generate_wp_post(self, post_data):
        data = PostWpModel()
        data.post_author = self.user_id
        data.post_date = datetime.now()
        data.post_date_gmt = datetime.now()
        #converts imageUrl to html image
        data.post_content = self.__generate_data_wp_content(post_data.contentUrl, post_data.contentType)
        data.post_title = post_data.title
        data.post_excerpt = ""
        data.ping_status = "closed"
        data.post_status = "publish"
        data.comment_status = "open"
        data.post_password = ""
        data.post_name = self.__create_post_name(post_data.title)
        data.to_ping = ""
        data.pinged = ""
        data.post_modified = datetime.now()
        data.post_modified_gmt = datetime.now()
        data.post_content_filtered = ""
        data.post_parent = 0 #??
        data.guid = "invalid"
        data.menu_order = 1
        data.post_type = "post"
        data.post_mime_type = "" #??
        data.comment_count = 0
        return data

    def __create_post_name(self, title):
        #TODO: replace with proper regular expression
        return title.strip().replace(".", "")\
            .replace("*", "")\
            .replace(",", "")\
            .replace("(", "")\
            .replace(")", "")\
            .replace("!", "")\
            .replace("!", "")\
            .replace("!", "")\
            .replace("/", "")\
            .replace("?", "")\
            .replace("'", "")\
            .replace("&", "")\
            .replace("@", "")\
            .replace("#", "")\
            .replace("$", "")\
            .replace("%", "")\
            .replace("^", "")\
            .replace("|", "")\
            .replace(">", "")\
            .replace("<", "")\
            .replace("\\", "")\
            .replace("\"", "")\
            .replace(";", "")\
            .replace(":", "")\
            .replace("~", "")\
            .replace("]", "")\
            .replace("“", "")\
            .replace("[", "")\
            .replace(" ", "-")\



    def __execute_insert(self, cursor, add_post_query, wp_post):
        cursor.execute(add_post_query,
                       (wp_post.post_author, wp_post.post_date, wp_post.post_date_gmt, wp_post.post_content, wp_post.post_title,
                        wp_post.post_excerpt, wp_post.post_status, wp_post.ping_status, wp_post.comment_status, wp_post.post_password,
                        wp_post.post_name, wp_post.to_ping, wp_post.pinged, wp_post.post_modified, wp_post.post_modified_gmt,
                        wp_post.post_content_filtered, wp_post.post_parent, 'invalid', wp_post.menu_order, wp_post.post_type,
                        wp_post.post_mime_type, wp_post.comment_count))

    def __insert_likes(self, cursor, insert_likes_query, post_id, likes):
        cursor.execute(insert_likes_query, (post_id, likes))

    def __generate_data_wp_content(self, contentUrl, contentType):
        if contentType == "image":
            return "<img class='size-full' " + "src='" + contentUrl + "' alt='custard' />"
        if contentType == "video/mp4":
            return contentUrl

    def __get_add_post_query(self):
        return ("""INSERT INTO `n4dlol1_wp`.`wp_posts`
                    (`post_author`,
                    `post_date`,
                    `post_date_gmt`,
                    `post_content`,
                    `post_title`,
                    `post_excerpt`,
                    `post_status`,
                    `comment_status`,
                    `ping_status`,
                    `post_password`,
                    `post_name`,
                    `to_ping`,
                    `pinged`,
                    `post_modified`,
                    `post_modified_gmt`,
                    `post_content_filtered`,
                    `post_parent`,
                    `guid`,
                    `menu_order`,
                    `post_type`,
                    `post_mime_type`,
                    `comment_count`)
                    VALUES
                    (%s, %s, %s, %s, %s, %s,
                     %s, %s, %s, %s, %s, %s,
                     %s, %s, %s, %s, %s, %s,
                     %s, %s, %s, %s
                     )
                     """)

    def __get_update_post_guid_query(self):
        return '''UPDATE wp_posts
        SET guid =  CONCAT('http://www.4dlols.com/?p=', CAST(ID as char))
        where guid like 'invalid' '''

    def __get_check_if_post_exists_query(self):
        return ("SELECT COUNT(Id) FROM wp_posts WHERE post_content LIKE %(contentUrl)s")

    def __get_insert_likes_query(self):
        return '''INSERT INTO `n4dlol1_wp`.`wp_postmeta`
                                (`post_id`,
                                `meta_key`,
                                `meta_value`)
                                VALUES
                                (%s,'_liked', %s);'''

