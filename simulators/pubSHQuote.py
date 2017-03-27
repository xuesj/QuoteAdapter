# -*- coding: utf-8 -*-
"""Simulator to publish Shanghai Exchange quotes through file 'mktdt00.txt'"""

import os.path
import time

PUB_FILE = '../datas/mktdt00.txt'
SOURCE_FILES = ['../datas/index_data.txt',
                '../datas/stock_data.txt',
                '../datas/bond_data.txt',
                '../datas/fund_data.txt',
                '../datas/tail_data.txt']


def get_head(seq):
    BeginString = 'HEADER'
    Version = 'MTP1.00 '
    BodyLength = '      1000'
    TotNumTradeReports = '00001'
    seq_str = str(seq)
    MDReportID = ' ' * (8 - len(seq_str)) + seq_str
    SenderCompID = '123456'
    MDTime = '21070327-09:45:28.001'
    MDUpdateType = '0'
    MDSesStatus = '12345678'
    head_str = BeginString + '|' + \
               Version + '|' + \
               BodyLength + '|' + \
               TotNumTradeReports + '|' + \
               MDReportID + '|' + \
               SenderCompID +'|' + \
               MDTime + '|' + \
               MDUpdateType + '|' + \
               MDSesStatus + '\n'
    return head_str


def get_line(source_file):
    if not os.path.exists(source_file):
        print('File is not exist!')
        return None

    with open(source_file, 'r') as f:
        msg = f.read()

    return msg


def get_lines():
    msg = ''
    for source_file in SOURCE_FILES:
        msg += get_line(source_file)
    return msg


def pub_quotes(pub_file):
    lines = get_lines()
    i = 0
    while True:
        i += 1
        msg = get_head(i)
        msg = msg + lines
        print('Publish Msg: ' + str(i))

        with open(pub_file, 'w') as f:
            f.write(msg)
        time.sleep(1)
        if i >= 30:
            break

if __name__ == '__main__':
    pub_quotes(PUB_FILE)
