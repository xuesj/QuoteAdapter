# -*- coding: utf-8 -*-
"""Simulator to publish Shanghai Exchange quotes through file 'mktdt00.txt'"""

import os.path
import time
import fcntl

PUB_FILE = '../datas/mktdt00.txt'
EQUITY_FILES = ['../datas/index_data.txt',
                '../datas/stock_data.txt',
                '../datas/bond_data.txt',
                '../datas/fund_data.txt']
TAIL_FILE = ['../datas/tail_data.txt']


def get_head(seq):
    BeginString = 'HEADER'
    Version = 'MTP1.00 '
    BodyLength = '      1000'
    TotNumTradeReports = '0' * (6 - len(str(seq))) + str(seq)
    MDReportID = ' ' * (8 - len(str(seq))) + str(seq)
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


def get_index(seq):
    MDStreamID = 'MD001'
    SecurityID = '0' * (6 - len(str(seq))) + str(seq)
    Symbol = 'SFZ     '
    TradeVolume = '     10000000000'
    TotalValueTraded = '       600000.01'
    PreClosePx = '100000.0001'
    OpenPrice = '200000.0002'
    HighPrice = '300000.0003'
    LowPrice = '400000.0004'
    TradePrice = '500000.0005'
    ClosePx = '600000.0006'
    TradePhaseCode = '12345678'
    Timestamp = '22:10:20.001'

    msg = MDStreamID + '|' + \
        SecurityID + '|' + \
        Symbol + '|' + \
        TradeVolume + '|' + \
        TotalValueTraded + '|' + \
        PreClosePx + '|' + \
        OpenPrice + '|' + \
        HighPrice + '|' + \
        LowPrice + '|' + \
        TradePrice + '|' + \
        ClosePx + '|' + \
        TradePhaseCode + '|' + \
        Timestamp + '\n'
    return msg


def get_line(seq, conf):
    with open(conf, 'r') as f:
        values = f.readline().split('|')
    values[1] = '0' * (6 - len(str(seq))) + str(seq)
    msg = values[0]
    for i in range(1, len(values)):
        msg = msg + '|' + values[i]
    return msg


def read_line(source_file):
    if not os.path.exists(source_file):
        print('File is not exist!')
        return None

    with open(source_file, 'r') as f:
        msg = f.read()

    return msg


def read_lines(source_file):
    msg = ''
    for source_file in source_file:
        msg += read_line(source_file)
    return msg


def pub_quotes(pub_file):
    j = 0
    lines = ''
    for data_file in EQUITY_FILES:
        j += 1
        lines += get_line(j, data_file)

    # lines = read_lines(EQUITY_FILES)
    tail = read_lines(TAIL_FILE)
    i = 0
    m = 3000
    while True:
        i += 1
        msg = get_head(i)
        msg = msg + lines
        j = 5
        for data_file in EQUITY_FILES:
            for k in range(m):
                msg += get_line(j + k, data_file)
            j += m
        msg += tail

        print('Publish Msg: ' + str(i))

        with open(pub_file, 'w+') as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            f.write(msg)
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)
        time.sleep(0.75)
        if i >= 30:
            break

if __name__ == '__main__':
    pub_quotes(PUB_FILE)
