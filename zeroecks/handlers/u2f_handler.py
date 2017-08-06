from tornado import gen
from tornado.web import authenticated
from tornado.options import options
from collections import namedtuple
from u2flib_server.u2f import (begin_registration, begin_authentication,
                               complete_registration, complete_authentication)
from . import BaseHandler


class U2FAuthHandler(BaseHandler):

    @authenticated
    @gen.coroutine
    def get(self):
        begin_authentication()

    @authenticated
    @gen.coroutine
    def post(self):
        complete_authentication()


class U2FRegisterHandler(BaseHandler):

    @authenticated
    @gen.coroutine
    def get(self):
        # Get Registered keys
        Record = namedtuple('Record', 'version, keyHandle, transports, appId')

        with self.dbref.cursor() as cursor:
            cursor.execute('''
            select  version,
                    keyHandle,
                    transports,
                    appId
            from site.u2f_devices
            where user_name = %s
            ''', (self.current_user,))

            devices = [dict(version=d.version,
                            keyHandle=d.keyHandle,
                            appId=d.appId) for
                       d in map(Record._make, cursor.fetchall())]

        challenge = begin_registration(options.u2f_app_id, devices)
        self.redis.set(self.current_user, challenge.json)

        self.write(challenge.data_for_client)

    @authenticated
    @gen.coroutine
    def post(self):
        key_nick = self.get_argument('keynick')
        device_response = self.get_argument('deviceResponse')

        challenge = self.redis.get(self.current_user)
        self.redis.delete(self.current_user)

        device, certificate = complete_registration(challenge, device_response)

        with self.dbref.cursor() as cursor:
            cursor.execute('''
            insert into site.u2f_devices (
                user_name, key_nick, version, keyhandle, publickey,
                transports, appid )
            values (%s, %s, %s, %s, %s, %s, %s)
            ''', (self.current_user, key_nick,
                  device.get('version'),
                  device.get('keyHandle'),
                  device.get('publicKey'),
                  device.get('transports'),
                  device.get('appId')))

        self.write(device)
