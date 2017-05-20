from tornado.web import UIModule


class Article(UIModule):

    def render(self, article):
        return self.render_string('article_module.tmpl.html',
                                  article=article)
