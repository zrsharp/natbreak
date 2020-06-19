# -*- coding: utf-8 -*-

import pymysql

USER_TABLE = 'user_user'
DB_HOST = 'zerohost'
DB_USER = 'zero'
DB_PASSWD = 'zero'
DB_NAME = 'natbreak'


class User:
    def __init__(self, username, password):
        self._username = username
        self._password = password

    def __str__(self):
        return 'id: %s, username: %s, _passwd: %s' % (
            self._user_id, self._username, self._password)

    def login(self):
        success = False
        conn = None
        cursor = None
        try:
            conn = pymysql.connect(DB_HOST, DB_USER, DB_PASSWD, DB_NAME)
            cursor = conn.cursor()
            sql = "SELECT * FROM " + USER_TABLE + " u" \
                    " WHERE u.username = '%s' AND u.password = '%s'" \
                    % (self._username, self._password)
            print(sql)
            cursor.execute(sql)

            cursor.fetchall()
            if cursor.rowcount != 0:
                print('login verify success.')
                success = True
            else:
                print('login verify fail.')
            return success
        except pymysql.Error as e:
            print(e.args[0], e.args[1])
            success = False
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()
