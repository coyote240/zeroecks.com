import tornado
from tornado.testing import AsyncHTTPTestCase, gen_test
from tornado.options import options
from .. import application


class TestApplication(AsyncHTTPTestCase):

    def get_app(self):
        app = application.Application()
        app.settings['template_path'] = 'foo'
        print(app.settings)
        return app

    def test_config(self):
        self.assertEqual(options.template_path, 'zeroecks/templates')

    @gen_test
    def test_index(self):
        response = self.fetch('/')
        server = response.headers.get('Server')

        self.assertEqual(response.code, 200)
        self.assertEqual(server, 'TornadoServer/{}'.format(tornado.version))
