from tornado.web import UIModule


class U2FModule(UIModule):

    def javascript_files(self):
        return ['js/profile.js']

    def css_files(self):
        return ['css/u2f.css']

    def render(self):
        return self.render_string('u2f_module.tmpl.html')
