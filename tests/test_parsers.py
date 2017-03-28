# -*- coding: UTF-8 -*-

import datetime

from parsers.Parsers import Parser, IntParser, StringParser, FloatParser, DatetimeParser, TimeParser
from parsers.Parsers import SnapshotParser, LineParser
from parsers.Quotes import QuoteSnapshot, Quote
from utils import Exchange, Protocol


def test_field_parser():
    c_rule = 'C6'
    i_rule = 'N8'
    f_rule = 'F8(3)'
    d_rule = 'D21'
    t_rule = 'T12'
    ex = Exchange.SH
    protocol = Protocol.FILE

    parser1 = Parser.get_field_parser(ex, protocol, c_rule)
    parser2 = Parser.get_field_parser(ex, protocol, i_rule)
    parser3 = Parser.get_field_parser(ex, protocol, f_rule)
    parser4 = Parser.get_field_parser(ex, protocol, d_rule)
    parser5 = Parser.get_field_parser(ex, protocol, t_rule)

    assert isinstance(parser1, StringParser)
    assert isinstance(parser2, IntParser)
    assert isinstance(parser3, FloatParser)
    assert isinstance(parser4, DatetimeParser)
    assert isinstance(parser5, TimeParser)

    msg1 = 'Hello     '
    msg2 = '     123'
    msg3 = '    123.54'
    msg4 = '1234.56   '
    msg5 = '20170323-20:10:30.001'
    dt = datetime.datetime(2017, 3, 23, 20, 10, 30, 1)
    msg6 = '20:10:30.001'
    tm = datetime.time(20, 10, 30, 1)

    assert parser1.parse(msg1) == 'Hello'
    assert parser2.parse(msg2) == 123
    assert parser3.parse(msg3) == 123.54
    assert parser3.parse(msg4) == 1234.56
    assert parser4.parse(msg5) == dt
    assert parser5.parse(msg6) == tm


def test_line_parser():
    """Test head_parser"""
    data_file = '../datas/head_data.txt'
    conf_file = '../datas/head_rule.conf'
    ex = Exchange.SH
    protocol = Protocol.FILE
    line_type = LineParser.HEAD
    parser = LineParser(ex, protocol, conf_file, line_type)
    with open(data_file, 'r') as f:
        line = f.readline()
        d = parser.parse(line)

    assert d
    assert isinstance(d, QuoteSnapshot)

    """Test index_parser"""
    data_file = '../datas/index_data.txt'
    conf_file = '../datas/index_rule.conf'
    ex = Exchange.SH
    protocol = Protocol.FILE
    line_type = LineParser.INDEX
    parser = LineParser(ex, protocol, conf_file, line_type)
    assert isinstance(parser, LineParser)

    with open(data_file, 'r') as f:
        line = f.readline()
        d = parser.parse(line)

    assert d
    assert isinstance(d, Quote)

    assert d.symbol == 'AAPL'
    assert d.volume == 10000
    assert d.amount == 123456.78
    assert d.last == 101.0001
    assert d.open == 102.0002
    assert d.high == 103.0003
    assert d.low == 104.0004
    assert d.price == 105.0005
    assert d.close == 106.006
    assert d.dt == datetime.datetime.combine(datetime.datetime.today().date(),
                                             datetime.time(22, 10, 30, 1))

    """Test stcok_parser"""
    data_file = '../datas/stock_data.txt'
    conf_file = '../datas/stock_rule.conf'
    ex = Exchange.SH
    protocol = Protocol.FILE
    line_type = LineParser.STOCK
    parser = LineParser(ex, protocol, conf_file, line_type)
    assert isinstance(parser, LineParser)

    with open(data_file, 'r') as f:
        line = f.readline()
        d = parser.parse(line)

    assert d
    assert isinstance(d, Quote)

    assert d.symbol == 'BAPL'
    assert d.volume == 10000
    assert d.amount == 123456.78
    assert d.last == 101.001
    assert d.open == 102.002
    assert d.high == 103.003
    assert d.low == 104.004
    assert d.price == 105.005
    assert d.close == 106.006
    assert d.dt == datetime.datetime.combine(datetime.datetime.today().date(),
                                             datetime.time(22, 10, 30, 1))
    assert d.buy_bids['Buy1']['Price'] == 201.001
    assert d.buy_bids['Buy1']['Volume'] == 201
    assert d.buy_bids['Buy2']['Price'] == 202.002
    assert d.buy_bids['Buy2']['Volume'] == 202
    assert d.buy_bids['Buy3']['Price'] == 203.003
    assert d.buy_bids['Buy3']['Volume'] == 203
    assert d.buy_bids['Buy4']['Price'] == 204.004
    assert d.buy_bids['Buy4']['Volume'] == 204
    assert d.buy_bids['Buy5']['Price'] == 205.005
    assert d.buy_bids['Buy5']['Volume'] == 205

    assert d.sell_bids['Sell1']['Price'] == 301.001
    assert d.sell_bids['Sell1']['Volume'] == 301
    assert d.sell_bids['Sell2']['Price'] == 302.002
    assert d.sell_bids['Sell2']['Volume'] == 302
    assert d.sell_bids['Sell3']['Price'] == 303.003
    assert d.sell_bids['Sell3']['Volume'] == 303
    assert d.sell_bids['Sell4']['Price'] == 304.004
    assert d.sell_bids['Sell4']['Volume'] == 304
    assert d.sell_bids['Sell5']['Price'] == 305.005
    assert d.sell_bids['Sell5']['Volume'] == 305

    """Test bond_parser"""
    data_file = '../datas/bond_data.txt'
    conf_file = '../datas/stock_rule.conf'
    ex = Exchange.SH
    protocol = Protocol.FILE
    line_type = LineParser.STOCK
    parser = LineParser(ex, protocol, conf_file, line_type)
    assert isinstance(parser, LineParser)

    with open(data_file, 'r') as f:
        line = f.readline()
        d = parser.parse(line)

    assert d
    assert isinstance(d, Quote)

    assert d.symbol == 'CAPL'
    assert d.volume == 10000
    assert d.amount == 123456.78
    assert d.last == 101.001
    assert d.open == 102.002
    assert d.high == 103.003
    assert d.low == 104.004
    assert d.price == 105.005
    assert d.close == 106.006
    assert d.dt == datetime.datetime.combine(datetime.datetime.today().date(),
                                             datetime.time(22, 10, 30, 1))

    """Test fund_parser"""
    data_file = '../datas/fund_data.txt'
    conf_file = '../datas/stock_rule.conf'
    ex = Exchange.SH
    protocol = Protocol.FILE
    line_type = LineParser.STOCK
    parser = LineParser(ex, protocol, conf_file, line_type)
    assert isinstance(parser, LineParser)

    with open(data_file, 'r') as f:
        line = f.readline()
        d = parser.parse(line)

    assert d
    assert isinstance(d, Quote)

    assert d.symbol == 'DAPL'
    assert d.volume == 10000
    assert d.amount == 123456.78
    assert d.last == 101.001
    assert d.open == 102.002
    assert d.high == 103.003
    assert d.low == 104.004
    assert d.price == 105.005
    assert d.close == 106.006
    assert d.dt == datetime.datetime.combine(datetime.datetime.today().date(),
                                             datetime.time(22, 10, 30, 1))

    """Test tail_parser"""
    data_file = '../datas/tail_data.txt'
    conf_file = '../datas/tail_rule.conf'
    ex = Exchange.SH
    protocol = Protocol.FILE
    line_type = LineParser.TAIL
    parser = LineParser(ex, protocol, conf_file, line_type)
    assert isinstance(parser, LineParser)

    with open(data_file, 'r') as f:
        line = f.readline()
        d = parser.parse(line)

    assert len(d) == 2
    assert d['EndingString'] == 'TRAILER'
    assert d['CheckSum'] == 'ABC'


def get_snapshot_parser():
    exchange = Exchange.SH
    protocol = Protocol.FILE
    port = '../datas/mktdt00.txt'
    head = '../datas/head_rule.conf'
    index = '../datas/index_rule.conf'
    stock = '../datas/stock_rule.conf'
    bond = '../datas/stock_rule.conf'
    fund = '../datas/stock_rule.conf'
    tail = '../datas/tail_rule.conf'

    snapshot_parser = SnapshotParser(exchange, protocol, port, head, index, stock, bond, fund, tail)
    return snapshot_parser


def test_snapshot():
    snapshot_parser = get_snapshot_parser()
    msg = snapshot_parser.get_msg()
    snapshot = snapshot_parser.parse(msg)

    assert isinstance(snapshot, QuoteSnapshot)
    # assert len(snapshot.quotes) == 4
    assert snapshot.quotes['000001']
    assert snapshot.quotes['000001'].equity == '000001'
    assert snapshot.quotes['000002'].equity == '000002'
    assert snapshot.quotes['000003'].equity == '000003'
    assert snapshot.quotes['000004'].equity == '000004'
