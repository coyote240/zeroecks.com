from tornado.web import UIModule


class FileUpload(UIModule):

    def javascript_files(self):
        return ['js/file-upload.js']

    def render(self):
        return self.render_string('file_upload.tmpl.html',
                                  xsrf_token=self.handler.xsrf_token)
