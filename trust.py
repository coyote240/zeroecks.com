#!/usr/bin/env python

import gnupg
import pprint


gpg = gnupg.GPG(homedir='./test')

with open('test/aags.asc', 'r') as key_file:
    key = key_file.read()
    gpg.import_keys(key)

pubkeys = gpg.list_keys()

for key in pubkeys:
    pprint.pprint(gpg.list_sigs(key.get('keyid')))
