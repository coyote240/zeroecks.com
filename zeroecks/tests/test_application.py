import tornado
import tornado.options
import tornado.testing
from .. import application


class TestApplication(tornado.testing.AsyncHTTPTestCase):

    def get_app(self):
        tornado.options.options.config = 'conf/config.py'
        tornado.options.options.debug = False

        return application.Application()

    def test_init_handlers(self):
        pass

    def test_index(self):
        response = self.fetch('/')
        server = response.headers.get('Server')

        self.assertEqual(response.code, 200)
        self.assertEqual(server, 'TornadoServer/{}'.format(tornado.version))
        self.stop()
