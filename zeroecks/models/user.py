import uuid
import hashlib
import binascii
from tornado import gen


class User(object):

    def __init__(self, connection):
        self.connection = connection

    @gen.coroutine
    def authorize(self, userid, password):
        (salt,) = yield self.get_salt(userid)
        if salt is None:
            return None

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

        return res

    @gen.coroutine
    def create(self, userid, password):
        hashed_password = self.hash_password(password)

        with self.connection.cursor() as cursor:
            cursor.execute('''
            insert into site.users (user_name, password)
            values (%s, %s)
            returning id
            ''', (userid, hashed_password))

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

        return res

    def hash_password(self, password, salt=None):
        if salt is None:
            salt = uuid.uuid4().hex

        dk = hashlib.pbkdf2_hmac('sha512',
                                 bytes(password, 'utf-8'),
                                 bytes.fromhex(salt),
                                 100000)
        return binascii.hexlify(dk).decode()
