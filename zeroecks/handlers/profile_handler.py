from tornado import gen
from tornado.web import HTTPError, authenticated
from . import BaseHandler
from ..models import User


class ProfileHandler(BaseHandler):

    def prepare(self):
        self.user = User(self.dbref)

    @authenticated
    @gen.coroutine
    def get(self):
        profile = yield self.user.get_profile(self.current_user)
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
                        last_login=last_login)
            return

        raise HTTPError(status_code=404,
                        log_message='Profile not found',
                        reason='Profile not found')

    @gen.coroutine
    def change_password(self, old_pwd, new_pwd):
        pass
