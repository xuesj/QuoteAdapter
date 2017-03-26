# -*- coding: UTF-8 -*-
import abc
from collections import defaultdict
import datetime
import time
from utils import Exchange, Protocol, ExChangeStatus, Market, EquityCategory, EquityStatus
from parsers.Quotes import QuoteSnapshot, Quote


class Parser(object):
    """Abstract Class of Parser"""
    PADDING_LEFT = 0
    PADDING_RIGHT = 1

    __metaclass__ = abc.ABCMeta

    def __init__(self, exchange, protocol):
        self._parse_rules = defaultdict(dict)
        self._exchange = exchange
        self._protocol = protocol

    @abc.abstractmethod
    def parse(self, msg):
        pass

    @classmethod
    def get_field_parser(cls, ex, protocol, parse_rule):
        field_parsers = {
            'C': StringParser,
            'N': IntParser,
            'F': FloatParser,
            'D': DatetimeParser,
            'T': TimeParser
        }
        leading = parse_rule[0]
        return field_parsers[leading](ex, protocol, parse_rule)

    @classmethod
    def handle_head(cls, ex, protocol, dict_value):
        if ex == Exchange.SH and protocol == Protocol.FILE:
            dt = dict_value['MDTime']
            status = ExChangeStatus.OPEN  # to do for dict_value['MDSesStatus']
            quote_snapshot = QuoteSnapshot(ex,
                                           dt,
                                           status
                                           )
            return quote_snapshot
        else:
            return None                   # to do for other types

    @classmethod
    def handle_quote(cls, ex, protocol, value):
        if ex == Exchange.SH and protocol == Protocol.FILE:
            exchange = ex
            market = Market.ALL
            equity = value['SecurityID']
            symbol = value['Symbol']
            category = EquityCategory.INDEX
            status = EquityStatus.TRADE
            dt = datetime.datetime.combine(datetime.datetime.today().date(),
                                           value['Timestamp'])
            volume = value['TradeVolume']
            amount = value['TotalValueTraded']
            last = value['PreClosePx']
            open_price = value['OpenPrice']
            high = value['HighPrice']
            low = value['LowPrice']
            price = value['TradePrice']
            close_price = value['ClosePx']
            timestamp = time.time()
            quote = Quote(exchange,
                          market,
                          equity,
                          symbol,
                          category,
                          status,
                          dt,
                          volume,
                          amount,
                          last,
                          open_price,
                          high,
                          low,
                          price,
                          close_price,
                          timestamp
                          )
            return quote
        else:
            return None                   # to do for other types

    @classmethod
    def handle_index(cls, ex, protocol, value):
        return cls.handle_quote(ex, protocol, value)

    @classmethod
    def handle_stock(cls, ex, protocol, value):
        quote = cls.handle_quote(ex, protocol, value)

        quote.buy_bids['Buy1'] = {'Price': value['BuyPrice1'],
                                  'Volume': value['BuyVolume1']}
        quote.buy_bids['Buy2'] = {'Price': value['BuyPrice2'],
                                  'Volume': value['BuyVolume2']}
        quote.buy_bids['Buy3'] = {'Price': value['BuyPrice3'],
                                  'Volume': value['BuyVolume3']}
        quote.buy_bids['Buy4'] = {'Price': value['BuyPrice4'],
                                  'Volume': value['BuyVolume4']}
        quote.buy_bids['Buy5'] = {'Price': value['BuyPrice5'],
                                  'Volume': value['BuyVolume5']}

        quote.sell_bids['Sell1'] = {'Price': value['SellPrice1'],
                                    'Volume': value['SellVolume1']}
        quote.sell_bids['Sell2'] = {'Price': value['SellPrice2'],
                                    'Volume': value['SellVolume2']}
        quote.sell_bids['Sell3'] = {'Price': value['SellPrice3'],
                                    'Volume': value['SellVolume3']}
        quote.sell_bids['Sell4'] = {'Price': value['SellPrice4'],
                                    'Volume': value['SellVolume4']}
        quote.sell_bids['Sell5'] = {'Price': value['SellPrice5'],
                                    'Volume': value['SellVolume5']}

        return quote

    @classmethod
    def handle_fund(cls, ex, protocol, value):
        return cls.handle_stock(ex, protocol, value)

    @classmethod
    def handle_bond(cls, ex, protocol, value):
        return cls.handle_stock(ex, protocol, value)

    @classmethod
    def handle_tail(cls, ex, protocol, value):
        return value


class StringParser(Parser):
    def __init__(self, exchange, protocol, parse_rule):
        super(StringParser, self).__init__(exchange, protocol)
        leading, msg_len = parse_rule[0], int(parse_rule[1:])
        assert leading == 'C'
        assert isinstance(msg_len, int)
        self._parse_rules['leading'] = leading
        self._parse_rules['length'] = msg_len
        self._parse_rules['padding'] = Parser.PADDING_RIGHT
        self._parse_rules['desc'] = 'CX: space padding right'

    def parse(self, msg):
        str_length = self._parse_rules['length']
        if self._parse_rules['padding'] == Parser.PADDING_RIGHT:
            return msg[:str_length]
        elif self._parse_rules['padding'] == Parser.PADDING_LEFT:
            return msg[-str_length:]
        else:
            raise TypeError


class IntParser(Parser):
    def __init__(self, exchange, protocol, parse_rule):
        super(IntParser, self).__init__(exchange, protocol)
        leading, msg_len = parse_rule[0], int(parse_rule[1:])
        assert leading == 'N'
        assert isinstance(msg_len, int)
        self._parse_rules['leading'] = leading
        self._parse_rules['length'] = msg_len
        self._parse_rules['padding'] = Parser.PADDING_LEFT
        self._parse_rules['desc'] = 'NX: space padding left'

    def parse(self, msg):
        pos = self._parse_rules['length']
        if self._parse_rules['padding'] == Parser.PADDING_RIGHT:
            return int(msg[:pos])
        elif self._parse_rules['padding'] == Parser.PADDING_LEFT:
            return int(msg[-pos:])
        else:
            raise TypeError


class FloatParser(Parser):
    def __init__(self, exchange, protocol, parse_rule):
        super(FloatParser, self).__init__(exchange, protocol)
        leading = parse_rule[0]
        msg_len = int(parse_rule[1:parse_rule.find('(')])
        dec_len = int(parse_rule[parse_rule.find('(')+1:parse_rule.find(')')])
        assert leading == 'F'
        assert isinstance(msg_len, int)
        assert isinstance(dec_len, int)
        self._parse_rules['leading'] = leading
        self._parse_rules['msg_len'] = msg_len
        self._parse_rules['dec_int'] = dec_len
        self._parse_rules['padding'] = Parser.PADDING_LEFT
        self._parse_rules['desc'] = 'FX(Y): space padding left'

    def parse(self, msg):
        f = float(msg)
        assert isinstance(f, float)
        return f


class DatetimeParser(Parser):
    def __init__(self, exchange, protocol, parse_rule):
        super(DatetimeParser, self).__init__(exchange, protocol)
        leading, msg_len = parse_rule[0], int(parse_rule[1:])
        assert leading == 'D'
        assert isinstance(msg_len, int)
        self._parse_rules['leading'] = leading
        self._parse_rules['msg_len'] = msg_len
        self._parse_rules['padding'] = Parser.PADDING_LEFT
        self._parse_rules['desc'] = 'D21: YYYYMMDD-HH:MM:SS.000'

    def parse(self, msg):
        year = int(msg[0:4])
        month = int(msg[4:6])
        day = int(msg[6:8])
        hour = int(msg[9:11])
        minute = int(msg[12:14])
        second = int(msg[15:17])
        microsecond = int(msg[18:21])
        dt = datetime.datetime(year, month, day, hour, minute, second, microsecond)
        assert isinstance(dt, datetime.datetime)
        return dt


class TimeParser(Parser):
    def __init__(self, exchange, protocol, parse_rule):
        super(TimeParser, self).__init__(exchange, protocol)
        leading, msg_len = parse_rule[0], int(parse_rule[1:])
        assert leading == 'T'
        assert isinstance(msg_len, int)
        self._parse_rules['leading'] = leading
        self._parse_rules['msg_len'] = msg_len
        self._parse_rules['padding'] = Parser.PADDING_LEFT
        self._parse_rules['desc'] = 'T12: HH:MM:SS.000'

    def parse(self, msg):
        hour = int(msg[0:2])
        minute = int(msg[3:5])
        second = int(msg[6:8])
        microsecond = int(msg[9:12])
        dt = datetime.time(hour, minute, second, microsecond)
        assert isinstance(dt, datetime.time)
        return dt


class LineParser(Parser):
    """To parse a line of an Exchange's quote"""
    HEAD = 0
    INDEX = 1
    STOCK = 2
    BOND = 3
    FUND = 4
    TAIL = 5

    HANDLES = {HEAD: Parser.handle_head,
               INDEX: Parser.handle_index,
               STOCK: Parser.handle_stock,
               FUND: Parser.handle_fund,
               BOND: Parser.handle_bond,
               TAIL: Parser.handle_tail
               }

    def __init__(self, exchange, protocol, conf_file, line_type, msg_sep='|', conf_sep=','):
        super(LineParser, self).__init__(exchange, protocol)
        self._msg_sep = msg_sep
        self._conf_sep = conf_sep
        self._line_type = line_type
        self._rules = []
        self._set_rules(conf_file)

    @property
    def parse_rules(self):
        return self._rules

    def _set_rules(self, rule_file):
        sep = self._conf_sep
        ex = self._exchange
        protocol = self._protocol

        with open(rule_file, 'r') as f:
            name_list = f.readline().rstrip().split(sep)
            for line in f:
                d = defaultdict(dict)
                value_list = line.rstrip().split(sep)
                for name, value in zip(name_list, value_list):
                    d[name] = value
                d['Parser'] = Parser.get_field_parser(ex, protocol, d['Rule_String'])
                self._rules.append(d)
            self._rules.sort(key=lambda x: int(x[name_list[0]]))

    def parse(self, msg):
        d = defaultdict(dict)
        sep = self._msg_sep
        msg_list = msg.rstrip().split(sep)
        for rule, msg_item in zip(self._rules, msg_list):
            d[rule['Name']] = rule['Parser'].parse(msg_item)
            if rule['Value'] is not '':
                assert d[rule['Name']] == rule['Parser'].parse(rule['Value'])

        handle = LineParser.HANDLES[self._line_type]
        return handle(self._exchange, self._protocol, d)


class SnapshotParser(Parser):
    """the Parser to parse a quote snapshot"""

    def __init__(self, exchange, protocol, port, head, index, stock, bond, fund, tail):
        super(SnapshotParser, self).__init__(exchange, protocol)
        self._port = port
        self._head = head
        self._index = index
        self._stock = stock
        self._bond = bond
        self._fund = fund
        self._tail = tail

        self._head_parser = LineParser(exchange, protocol, head, LineParser.HEAD)
        self._index_parser = LineParser(exchange, protocol, index, LineParser.INDEX)
        self._stock_parser = LineParser(exchange, protocol, stock, LineParser.STOCK)
        self._bond_parser = LineParser(exchange, protocol, bond, LineParser.BOND)
        self._fund_parser = LineParser(exchange, protocol, fund, LineParser.FUND)
        self._tail_parser = LineParser(exchange, protocol, tail, LineParser.TAIL)

    def get_msg(self):
        with open(self._port, 'r') as f:
            msg = f.read()
        return msg

    def parse(self, msg):
        lines = msg.split('\n')
        snapshot = self._head_parser.parse(lines[0])
        for line in lines[1:-1]:
            if line[0:5] == 'MD001':
                quote = self._index_parser.parse(line)
                snapshot.quotes[quote.equity] = quote
            elif line[0:5] == 'MD002':
                quote = self._stock_parser.parse(line)
                snapshot.quotes[quote.equity] = quote
            elif line[0:5] == 'MD003':
                quote = self._bond_parser.parse(line)
                snapshot.quotes[quote.equity] = quote
            elif line[0:5] == 'MD004':
                quote = self._fund_parser.parse(line)
                snapshot.quotes[quote.equity] = quote
            else:
                raise ValueError
        d = self._tail_parser.parse(lines[-1])
        assert d['EndingString'] == 'TRAILER'
        assert d['CheckSum'] == 'ABC'
        return snapshot
