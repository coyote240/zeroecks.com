import tornado
import unittest.mock
from tornado.testing import AsyncHTTPTestCase
from tornado.options import options
from application import Application


class TestApplication(AsyncHTTPTestCase):

    def get_app(self):

        class TestApp(Application):

            def init_options(self):
                super().init_options()
                unittest.mock.patch.object(options.mockable(), 'config', 'config.py')

        return TestApp()

    def test_config(self):
        self.assertEqual(options.template_path, 'zeroecks/templates')

    def test_index(self):
        response = self.fetch('/')
        server = response.headers.get('Server')

        self.assertEqual(response.code, 200)
        self.assertEqual(server, 'TornadoServer/{}'.format(tornado.version))
