# -*- coding: utf-8 -*-
"""Simulator to publish Shanghai Exchange quotes through file 'mktdt00.txt'"""

import os.path
import time
import fcntl
from apscheduler.schedulers.blocking import BlockingScheduler


PUB_FILE = '../datas/mktdt00.txt'
HEAD_FILE = '../datas/head_data.txt'
INDEX_FILE = '../datas/index_data.txt'
STOCK_FILE = '../datas/stock_data.txt'
BOND_FILE = '../datas/bond_data.txt'
FUND_FILE = '../datas/fund_data.txt'
TAIL_FILE = '../datas/tail_data.txt'


def set_seq(seq, line, part):
    items = line.split('|')
    if part == 'Head':
        items[4] = ' ' * (8 - len(str(seq))) + str(seq)
    elif part == 'Equity':
        items[1] = '0' * (6 - len(str(seq))) + str(seq)
    msg = '|'.join(items)

    return msg


def get_data(source_file):
    if not os.path.exists(source_file):
        print('Data File is not exist!')
        return None

    with open(source_file, 'r') as f:
        msg = f.read()

    return msg


def quote_seq(seq, head, index, stock, bond, fund, tail, m=1000, k=5):
    msg = set_seq(seq, head, 'Head')
    msg += index
    for j in range(k, m + k):
        msg += set_seq(j, stock, 'Equity')
    for j in range(m + k, 2 * m + k):
        msg += set_seq(j, bond, 'Equity')
    for j in range(2 * m + k, 3 * m + k):
        msg += set_seq(j, fund, 'Equity')
    msg += tail
    return msg


def quotes():
    m = 2
    i = 0
    head = get_data(HEAD_FILE)
    index = get_data(INDEX_FILE)
    stock = get_data(STOCK_FILE)
    bond = get_data(BOND_FILE)
    fund = get_data(FUND_FILE)
    tail = get_data(TAIL_FILE)

    while True:
        i += 1
        msg = quote_seq(i, head, index, stock, bond, fund, tail, m)
        if i >= 5:
            break
        yield msg


def pub_quotes(pub_file):
    i = 0
    for data in quotes():
        i += 1
        print('Publish Msg: ' + str(i))
        with open(pub_file, 'w+') as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            f.write(data)
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)
        time.sleep(1)


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    start = reduce(lambda x, y: str(x) + ',' + str(y), range(0, 59, 10))
    scheduler.add_job(pub_quotes, 'cron', args=(PUB_FILE,), second=start)
    scheduler.start()
