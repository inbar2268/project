import select
import sqlite3
from os.path import exists


class Users:
    def __init__(self, tablename = "users", username="username",password = "password"):
        self.__tablename = tablename
        self.__password = password
        self.__username= username
        conn = sqlite3.connect('users.db')
        conn.execute('''CREATE TABLE IF NOT EXISTS USERS
                    (
                    username		TEXT    NOT NULL,
                    password	TEXT	NOT NULL
                    );''')

        conn.commit()
        conn.close()


    def insert_user(self,username,password):
        conn = sqlite3.connect('users.db')
        str_insert = "INSERT INTO " + self.__tablename + " (" + self.__username +"," + self.__password + ") VALUES (" +  "'" +username + "'" + "," + "'" +password +"'" +");"
        conn.execute(str_insert)
        conn.commit()
        conn.close()




