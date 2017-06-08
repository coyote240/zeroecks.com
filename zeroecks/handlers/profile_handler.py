from tornado import gen
from tornado.web import HTTPError, authenticated
from . import BaseHandler


class ProfileHandler(BaseHandler):

    @authenticated
    @gen.coroutine
    def get(self):
        profile = yield self.get_profile()
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
    def get_profile(self):
        cursor = self.dbref.cursor()
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
        ''', (self.current_user,))

        res = cursor.fetchone()
        cursor.close()

        return res

    @gen.coroutine
    def change_password(self, old_pwd, new_pwd):
        pass
