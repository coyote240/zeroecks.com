import datetime
import logging
from tornado.web import authenticated
from tornado.util import ObjectDict
from . import BaseHandler


class TrustHandler(BaseHandler):

    def initialize(self, gpg):
        self.gpg = gpg
        super().initialize()

    @authenticated
    def get(self):
        self.render('trust.tmpl.html')

    @authenticated
    def post(self):
        user_name = self.get_argument('user_name')
        armored_key = self.get_argument('armored_key')

        logging.info('initializing gpg')

        self.gpg.import_keys(armored_key)
        [pubkey] = self.gpg.list_keys()
        sigs = self.gpg.list_sigs(pubkey.get('keyid')).sigs

        expiry = datetime.datetime.fromtimestamp(
            float(pubkey.get('expires')))

        self.render('upload.tmpl.html',
                    user_name=user_name,
                    expiry=expiry,
                    sigs=sigs,
                    pubkey=ObjectDict(pubkey))
