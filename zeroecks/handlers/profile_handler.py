from tornado.web import HTTPError, authenticated
from handlers import BaseHandler


class ProfileHandler(BaseHandler):

    @authenticated
    def get(self):
        profile = self.get_profile()
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
        from users.users
        where user_name = %s
        ''', (self.current_user,))

        res = cursor.fetchone()
        cursor.close()

        return res