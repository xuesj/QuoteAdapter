# -*- coding: utf-8 -*-
"""SimulateServer to publish Shanghai Exchange quotes through file 'mktdt00.txt'"""

import os.path
import time
import fcntl
import SocketServer


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
    m = 10
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


class SHTCPHandler(SocketServer.BaseRequestHandler):
    """
    Handle quote message.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        seq = 1
        for data in quotes():
            try:
                self.request.sendall(data)
                print('Send msg: ' + str(seq))
                seq += 1
            except:
                break
            time.sleep(3)


if __name__ == '__main__':
    HOST, PORT = 'localhost', 9129
    # Create the server, binding to localhost on port 9129
    server = SocketServer.TCPServer((HOST, PORT), SHTCPHandler)
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
