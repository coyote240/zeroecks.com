import redis
import psycopg2
from tornado.options import options
import tornadobase.handlers


class BaseHandler(tornadobase.handlers.BaseHandler):

    def initialize(self):
        self.dbref = psycopg2.connect(dbname=options.dbname,
                                      user=options.dbuser,
                                      password=options.dbpass)
        self.redis = redis.StrictRedis(host='localhost',
                                       port=6379,
                                       db=0,
                                       decode_responses=True)

    @property
    def session(self):
        session_id = self.get_secure_cookie('session')
        if session_id is not None:
            return self.redis.hgetall(session_id)
        return None

    def get_current_user(self):
        session_id = self.get_secure_cookie('__id')
        if session_id is not None:
            self.redis.expire(session_id, options.session_timeout)
            return self.redis.hget(session_id, 'userid')
        return None

    def write_error(self, status_code, **kwargs):
        (http_error, error, stacktrace) = kwargs['exc_info']
        if not hasattr(error, 'reason'):
            reason = 'Something went wrong.'
        else:
            reason = error.reason

        self.render('errors/general.html',
                    status_code=status_code,
                    reason=reason)

    def on_finish(self):
        self.dbref.close()
