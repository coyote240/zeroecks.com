from tornadobase.handlers import BaseHandler


class ArticleHandler(BaseHandler):

    def get(self, id=None):
        self.render('article.tmpl.html', article=id)
