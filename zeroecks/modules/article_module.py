from tornado.web import UIModule


class Article(UIModule):

    def render(self, article):
        id, author, content, date_created = article

        return self.render_string('article_module.tmpl.html',
                                  id=id,
                                  author=author,
                                  date_created=date_created,
                                  content=content)
