import uuid
import hashlib
import binascii
from collections import namedtuple
from tornado import gen


class User(object):

    def __init__(self, connection):
        self.connection = connection

    @gen.coroutine
    def authorize(self, userid, password):
        salt = yield self.get_salt(userid)
        if salt is None:
            raise gen.Return(None)

        hashed_password = self.hash_password(password, salt)

        with self.connection.cursor() as cursor:
            cursor.execute('''
            select  user_name,
                    fingerprint
            from    site.users
            where   user_name = %s
            and     password = %s
            ''', (userid, hashed_password))

            res = cursor.fetchone()

        raise gen.Return(res)

    @gen.coroutine
    def record_login(self):
        pass

    @gen.coroutine
    def create(self, userid, password):
        salt = uuid.uuid4().hex
        hashed_password = self.hash_password(password, salt)

        with self.connection.cursor() as cursor:
            cursor.execute('''
            insert into site.users (user_name, password, salt)
            values (%s, %s, %s)
            returning id
            ''', (userid, hashed_password, salt))

            res = cursor.fetchone()

        return res

    @gen.coroutine
    def get_salt(self, userid):
        with self.connection.cursor() as cursor:
            cursor.execute('''
            select  salt
            from    site.users
            where   user_name = %s
            ''', (userid,))

            res = cursor.fetchone()

        if res is None:
            return res
        return res[0]

    @gen.coroutine
    def get_profile(self, userid):
        Record = namedtuple('Record', '''
            userid, keyid, armored_key, verified,
            date_verified, date_created, last_login''')

        cursor = self.connection.cursor()
        cursor.execute('''
        select  user_name,
                key_id,
                armored_key,
                verified,
                date_verified,
                date_created,
                last_login
        from site.users
        where user_name = %s
        ''', (userid,))

        res = cursor.fetchone()

        if res is None:
            return None
        return Record._make(res)

    def hash_password(self, password, salt=None):
        if salt is None:
            salt = uuid.uuid4().hex

        dk = hashlib.pbkdf2_hmac('sha512',
                                 bytes(password, 'utf-8'),
                                 bytes.fromhex(salt),
                                 100000)
        return binascii.hexlify(dk).decode()


def create_user():
    import argparse
    import psycopg2
    from tornado.options import options, define

    parser = argparse.ArgumentParser()
    parser.add_argument('username')
    parser.add_argument('password')
    parser.add_argument('--config', required=True)
    args = parser.parse_args()

    define('dbname', type=str)
    define('dbuser', type=str)
    define('dbpass', type=str)
    options.parse_config_file(args.config)

    dbref = psycopg2.connect(dbname=options.dbname,
                             user=options.dbuser,
                             password=options.dbpass)
    dbref.autocommit = True

    user = User(dbref)
    user.create(args.username, args.password)
