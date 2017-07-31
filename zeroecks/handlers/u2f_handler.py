from tornado.web import authenticated, HTTPError
from tornado.options import options
from u2flib_server.u2f import (begin_registration, begin_authentication,
                               complete_registration, complete_authentication)
from . import BaseHandler


class U2FHandler(BaseHandler):

    def prepare(self):
        self.action = self.request.path[1:]

    def dispatch(self, name=None):
        if name is None:
            raise HTTPError(status_code=404,
                            log_message='Not Found',
                            reason='Not Found')
        action = getattr(self, name)
        return action()

    @authenticated
    def get(self):
        self.dispatch(self.action)

    def enroll(self):
        # Add Registered keys
        enroll = begin_registration(options.u2f_app_id, [])
        self.write(enroll)

    def bind(self):
        self.write('bind')

    def sign(self):
        self.write('sign')

    def verify(self):
        self.write('verify')
