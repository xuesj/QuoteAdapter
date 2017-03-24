# -*- coding: UTF-8 -*-

import datetime

from parsers.Parsers import Parser, IntParser, StringParser, FloatParser, DatetimeParser, TimeParser
from utils import Exchange, Port, Protocol
from parsers.Parsers import LineParser, QuoteSnapshot


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
    dt = datetime.datetime(2017, 03, 23, 20, 10, 30, 001)
    msg6 = '20:10:30.001'
    tm = datetime.time(20, 10, 30, 001)

    assert parser1.parse(msg1) == 'Hello '
    assert parser2.parse(msg2) == 123
    assert parser3.parse(msg3) == 123.54
    assert parser3.parse(msg4) == 1234.56
    assert parser4.parse(msg5) == dt
    assert parser5.parse(msg6) == tm


def test_line_parser():
    """Test head_parser"""
    data_file = '../datas/head_data.txt'
    conf_file = '../parsers/head_rule.conf'
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
    conf_file = '../parsers/index_rule.conf'
    ex = Exchange.SH
    protocol = Protocol.FILE
    line_type = LineParser.INDEX
    parser = LineParser(ex, protocol, conf_file, line_type)
    assert isinstance(parser, LineParser)
    with open(data_file, 'r') as f:
        line = f.readline()
        d = parser.parse(line)

    assert d
    assert d['MDStringID'] == 'MD001'
    assert d['Symbol'] == 'AAPL'
    assert d['TradeVolume'] == 10000

    """Test stcok_parser"""
    # index_data = '../datas/index_data.txt'
    conf_file = '../parsers/stock_rule.conf'
    ex = Exchange.SH
    protocol = Protocol.FILE
    line_type = LineParser.STOCK
    parser = LineParser(ex, protocol, conf_file, line_type)
    assert isinstance(parser, LineParser)

    """Test tail_parser"""
    # index_data = '../datas/index_data.txt'
    conf_file = '../parsers/tail_rule.conf'
    ex = Exchange.SH
    protocol = Protocol.FILE
    line_type = LineParser.TAIL
    parser = LineParser(ex, protocol, conf_file, line_type)
    assert isinstance(parser, LineParser)
