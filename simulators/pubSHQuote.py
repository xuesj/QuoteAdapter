# -*- coding: utf-8 -*-
"""Simulator to publish Shanghai Exchange quotes through file 'mktdt00.txt'"""

import os.path
import time

PUB_FILE = '../datas/mktdt00.txt'


def pub_quotes(file_name):
    if not os.path.exists(file_name):
        print(file_name + 'is not exist!')
        return

    print('Publishing SH Quotes ...')
    while True:
        with open(file_name, 'w') as f:
            f.write('Hello: ')
        time.sleep(1)

if __name__ == '__main__':
    pub_quotes(PUB_FILE)
