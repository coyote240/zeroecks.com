import uuid
from tornado import gen
from tornado.web import HTTPError
from tornado.options import options
from . import BaseHandler
from ..models import User


class AuthHandler(BaseHandler):

    def initialize(self, action=None):
        self.action = action
        super().initialize()

    def prepare(self):
        self.user = User(self.dbref)

    def get(self):
        if self.action is 'logout':
            self.clear_cookie('__id')
            self.redirect('/')
            return

        if self.current_user:
            self.redirect('/')
            return

        self.render('login.tmpl.html')

    @gen.coroutine
    def post(self):
        userid = self.get_argument('userid')
        password = self.get_argument('password')
        dest = self.get_argument('next', default='/')

        res = yield self.user.authorize(userid, password)

        if res is not None:
            (userid, fingerprint) = res
            self.set_session(userid, fingerprint)
            self.redirect(dest)
            return

        raise HTTPError(status_code=401,
                        log_message='Unauthorized',
                        reason='User name or password are incorrect')

    def set_session(self, userid, fingerprint):
        session_id = str(uuid.uuid4())
        self.redis.hmset(session_id, {
            'userid': userid,
            'fingerprint': fingerprint})
        self.redis.expire(session_id, options.session_timeout)
        self.set_secure_cookie('__id', session_id,
                               secure=True,
                               httponly=True)
