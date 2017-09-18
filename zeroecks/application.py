import tornadobase.application
from . import handlers
from . import modules

import tornado
from tornado.web import URLSpec
from tornado.options import define, options


define('dbname', type=str)
define('dbuser', type=str)
define('dbpass', type=str)
define('session_timeout', type=int, default=86400)
define('u2f_app_id', type=str)


class Application(tornadobase.application.Application):

    def init_settings(self):
        settings = super().init_settings()
        settings['ui_modules'] = modules
        settings['default_handler_class'] = handlers.NotFoundHandler

        return settings

    def init_handlers(self):

        self.handlers = [
            URLSpec(r'/',
                    handlers.IndexHandler,
                    name='Home'),
            URLSpec(r'/articles',
                    handlers.ArticleHandler,
                    name='Articles'),
            URLSpec(r'/articles/new',
                    handlers.NewArticleHandler,
                    name='NewArticle'),
            URLSpec(r'/articles/([0-9a-z-]*)',
                    handlers.ArticleHandler,
                    name='Article'),
            URLSpec(r'/articles/edit/([0-9a-z-]+)',
                    handlers.EditArticleHandler,
                    name='EditArticle'),
            URLSpec(r'/assets/',
                    handlers.StaticHandler,
                    name='Assets'),
            URLSpec(r'/login',
                    handlers.AuthHandler,
                    name='Login'),
            URLSpec(r'/logout',
                    handlers.AuthHandler,
                    {'action': 'logout'},
                    name='Logout'),
            URLSpec(r'/devices',
                    handlers.U2FDeviceHandler,
                    name='Devices'),
            URLSpec(r'/register',
                    handlers.U2FRegisterHandler,
                    name='Register'),
            URLSpec(r'/sign',
                    handlers.U2FAuthHandler,
                    name='Sign'),
            URLSpec(r'/profile',
                    handlers.ProfileHandler,
                    name='Profile')]

    def stop(self):
        tornado.ioloop.IOLoop.current().stop()


def main():
    options.parse_command_line()
    app = Application()
    app.start()
