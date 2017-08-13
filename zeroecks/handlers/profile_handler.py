from tornado import gen
from tornado.web import HTTPError, authenticated
from . import BaseHandler
from ..models import User, U2F


class ProfileHandler(BaseHandler):

    def prepare(self):
        self.user = User(self.dbref)
        self.u2f = U2F(self.dbref)

    def javascript_files(self):
        return ['js/profile.js']

    @authenticated
    @gen.coroutine
    def get(self):
        profile = yield self.user.get_profile(self.current_user)
        devices = yield self.u2f.registered_devices(self.current_user)

        if profile is not None:
            (userid, keyid, armored_key, verified, date_verified,
             date_created, last_login) = profile

            self.render('profile.tmpl.html',
                        userid=userid,
                        keyid=keyid,
                        armored_key=armored_key,
                        verified=verified,
                        date_verified=date_verified,
                        date_created=date_created,
                        last_login=last_login,
                        devices=devices)
            return

        raise HTTPError(status_code=404,
                        log_message='Profile not found',
                        reason='Profile not found')

    @authenticated
    @gen.coroutine
    def post(self):
        current_password = self.get_argument('current_password')
        new_password = self.get_argument('new_password')
        confirm_password = self.get_argument('confirm_password')

        if self.user.authorize(self.current_user, current_password) is None:
            self.warn('Authentication failed')
            raise HTTPError(status_code=402,
                            log_message='User not authorized',
                            reason='User not authorized')

        if new_password is not confirm_password:
            raise HTTPError(status_code=400,
                            log_message='Passwords must match',
                            reason='Passwords must match')

    @gen.coroutine
    def change_password(self, old_pwd, new_pwd):
        pass
