import uuid
import hashlib
from handlers import BaseHandler


class AuthHandler(BaseHandler):

    def get(self):
        if self.current_user:
            self.redirect('/')
        self.render('login.tmpl.html')

    def post(self):
        userid = self.get_argument('userid')
        password = self.get_argument('password')

        res = self.check_creds(userid, password)

        if res is not None:
            (userid, fingerprint) = res
            self.set_session(userid, fingerprint)
            self.redirect('/')

        self.set_status(401, reason='Unauthorized')
        self.render('login.tmpl.html')
        self.finish()

    def check_creds(self, userid, password):
        bpasswd = bytes(password, 'utf-8')
        hashed_password = hashlib.sha256(bpasswd).hexdigest()

        cursor = self.dbref.cursor()
        cursor.execute('''
        select  user_name,
                fingerprint
        from    users.users
        where   user_name = %s
        and     password = %s
        ''', (userid, hashed_password))

        res = cursor.fetchone()
        cursor.close()

        return res

    def set_session(self, userid, fingerprint):
        sessionid = str(uuid.uuid4())
        self.redis.hmset(sessionid, {
            'userid': userid,
            'fingerprint': fingerprint})
        self.set_secure_cookie('session', sessionid)
