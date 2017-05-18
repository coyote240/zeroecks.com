#!/usr/bin/env python

import hashlib
import secrets
import binascii
import argparse


def hash_password(raw_password):

    salt = secrets.token_bytes(16)
    dk = hashlib.pbkdf2_hmac('sha512',
                             bytes(raw_password, 'utf-8'),
                             salt, 100000)
    return (binascii.hexlify(salt), binascii.hexlify(dk))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('userid')
    parser.add_argument('password')
    args = parser.parse_args()

    salt, digest = hash_password('lostcity')
    print('salt: {0}\nhash: {1}'.format(
        salt.decode(), digest.decode()))
