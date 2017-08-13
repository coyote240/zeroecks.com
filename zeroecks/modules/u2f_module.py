from tornado.web import UIModule


class U2FModule(UIModule):

    def javascript_files(self):
        return ['js/u2f-api.js',
                'js/u2f_module.js']

    def css_files(self):
        return ['css/u2f.css']

    def render(self, devices):
        return self.render_string('u2f_module.tmpl.html',
                                  xsrf_token=self.handler.xsrf_token,
                                  devices=devices)
