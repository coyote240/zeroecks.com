from tornado.web import UIModule


class Article(UIModule):

    def render(self, article):
        return self.render_string(
            'article.tmpl.html', article=article)
