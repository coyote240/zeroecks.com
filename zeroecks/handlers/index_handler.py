from handlers import BaseHandler


class IndexHandler(BaseHandler):

    def get(self):
        self.render('index.tmpl.html')
