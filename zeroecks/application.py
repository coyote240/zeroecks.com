import tornadobase.application
from . import handlers
from . import modules

from tornado.web import URLSpec
from tornado.options import define


class Application(tornadobase.application.Application):

    def init_options(self):

        define('dbname', type=str)
        define('dbuser', type=str)
        define('dbpass', type=str)
        define('session_timeout', type=int, default=86400)

        super().init_options()

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
            URLSpec(r'/articles/([0-9]*)',
                    handlers.ArticleHandler,
                    name='Article'),
            URLSpec(r'/articles/new',
                    handlers.NewArticleHandler,
                    name='NewArticle'),
            URLSpec(r'/articles/edit/([0-9]+)',
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
            URLSpec(r'/profile',
                    handlers.ProfileHandler,
                    name='Profile')]


def main():
    app = Application()
    app.start()
