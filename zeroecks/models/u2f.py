from collections import namedtuple
from u2flib_server.u2f import (begin_registration, begin_authentication,
                               complete_registration, complete_authentication)
from tornado.options import options
from tornado import gen


class U2F(object):

    def __init__(self, dbref, redis=None):
        self.dbref = dbref
        self.redis = redis

    @gen.coroutine
    def registered_devices(self, user):
        Record = namedtuple('Record', ['key_nick',
                                       'publickey',
                                       'registration_date'])

        with self.dbref.cursor() as cursor:
            cursor.execute('''
            SELECT  key_nick,
                    publickey,
                    registration_date
            FROM    site.u2f_devices
            WHERE   user_name = %s
            ''', (user,))

            devices = map(Record._make, cursor.fetchall())

        raise gen.Return(devices)

    @gen.coroutine
    def get_registration_challenge(self, user):
        Record = namedtuple('Record', 'version, keyHandle, transports, appId')

        with self.dbref.cursor() as cursor:
            cursor.execute('''
            select  version,
                    keyHandle,
                    transports,
                    appId
            from site.u2f_devices
            where user_name = %s
            ''', (user,))

            devices = [dict(version=d.version,
                            keyHandle=d.keyHandle,
                            appId=d.appId) for
                       d in map(Record._make, cursor.fetchall())]

        challenge = begin_registration(options.u2f_app_id, devices)
        self.redis.set(user, challenge.json, ex=60)

        raise gen.Return(challenge.data_for_client)

    @gen.coroutine
    def register_device(self, user, key_nick, device_response):
        challenge = self.redis.get(user)
        self.redis.delete(user)

        device, certificate = complete_registration(challenge, device_response)

        with self.dbref.cursor() as cursor:
            cursor.execute('''
            insert into site.u2f_devices (
                user_name, key_nick, version, keyhandle, publickey,
                transports, appid )
            values (%s, %s, %s, %s, %s, %s, %s)
            ''', (user, key_nick,
                  device.get('version'),
                  device.get('keyHandle'),
                  device.get('publicKey'),
                  device.get('transports'),
                  device.get('appId')))

            raise gen.Return(device)

    @gen.coroutine
    def delete_device(self, user, nick):
        with self.dbref.cursor() as cursor:
            cursor.execute('''
            DELETE  FROM site.u2f_devices
            WHERE   user_name = %s
            AND     key_nick = %s
            ''', (user, nick))

            rowcount = cursor.rowcount

        raise gen.Return(rowcount)
