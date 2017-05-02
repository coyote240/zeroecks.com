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
                                       db=0)

    def get_current_user(self):
        session_id = self.get_secure_cookie('session')
        if session_id is not None:
            return self.redis.hget(session_id, 'userid')
        return None
