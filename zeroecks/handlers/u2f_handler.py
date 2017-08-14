from tornado import gen
from tornado.web import authenticated
from . import BaseHandler
from ..models import U2F


class U2FAuthHandler(BaseHandler):

    @authenticated
    @gen.coroutine
    def get(self):
        pass

    @authenticated
    @gen.coroutine
    def post(self):
        pass


class U2FRegisterHandler(BaseHandler):

    def prepare(self):
        self.u2f = U2F(self.dbref, self.redis)

    @authenticated
    @gen.coroutine
    def get(self):

        challenge = yield self.u2f.get_registration_challenge(
                self.current_user)

        self.write(challenge)

    @authenticated
    @gen.coroutine
    def post(self):
        key_nick = self.get_argument('keynick')
        device_response = self.get_argument('deviceResponse')

        device = yield self.u2f.register_device(self.current_user,
                                                key_nick,
                                                device_response)

        self.write(device)

    @authenticated
    @gen.coroutine
    def delete(self):
        key_nick = self.get_argument('key_nick')
        deleted = yield self.u2f.delete_device(self.current_user, key_nick)

        self.write({'deleted': deleted})
