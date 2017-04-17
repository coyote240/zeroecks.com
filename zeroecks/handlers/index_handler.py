import datetime
import tempfile
import logging
import gnupg
from tornado.util import ObjectDict
from tornadobase.handlers import BaseHandler


class IndexHandler(BaseHandler):

    def get(self):
        self.render('index.tmpl.html')

    def post(self):
        user_name = self.get_argument('user_name')
        armored_key = self.get_argument('armored_key')

        with tempfile.TemporaryDirectory() as homedir:
            logging.info('initializing gpg')
            gpg = gnupg.GPG(homedir=homedir)

            gpg.import_keys(armored_key)
            [pubkey] = gpg.list_keys()
            sigs = gpg.list_sigs(pubkey.get('keyid')).sigs

        expiry = datetime.datetime.fromtimestamp(
            float(pubkey.get('expires')))

        self.render('upload.tmpl.html',
                    user_name=user_name,
                    expiry=expiry,
                    sigs=sigs,
                    pubkey=ObjectDict(pubkey))
