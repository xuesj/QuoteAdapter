# -*- coding: utf-8 -*-
"""Simulator to publish Shanghai Exchange quotes through file 'mktdt00.txt'"""

import os.path
import time

PUB_FILE = '../datas/mktdt00.txt'
SOURCE_FILE = '../datas/head_conf.txt'


def pub_quotes(source_file, pub_file):
    if not (os.path.exists(pub_file) or os.path.exists(source_file)):
        print('File is not exist!')
        return

    print('Publishing SH Quotes ...')
    with open(source_file, 'r') as f:
        msg = f.read()

    while True:
        with open(pub_file, 'w') as f:
            f.write(msg)
        time.sleep(1)

if __name__ == '__main__':
    pub_quotes(SOURCE_FILE, PUB_FILE)
