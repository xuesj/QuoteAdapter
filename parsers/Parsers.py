# -*- coding: UTF-8 -*-
import abc
from collections import defaultdict
import datetime


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


class HeadParser(Parser):
    """To parse the head of Shanghai Exchange's quote file, e.g. mktdt00.txt"""
    def __init__(self, exchange, protocol, conf_file, msg_sep='|', conf_sep=','):
        super(HeadParser, self).__init__(exchange, protocol)
        self._msg_sep = msg_sep
        self._conf_sep = conf_sep
        self._rules = []
        self.set_rules(conf_file)

    @property
    def parse_rules(self):
        return self._rules

    def set_rules(self, rule_file):
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
            self._rules.sort(key=lambda x: x[name_list[0]])

    def parse(self, msg):
        d = defaultdict(dict)
        sep = self._msg_sep
        msg_list = msg.rstrip().split(sep)
        for rule, msg_item in zip(self._rules, msg_list):
            d[rule['Name']] = rule['Parser'].parse(msg_item)
            if rule['Value'] is not '':
                assert d[rule['Name']] == rule['Parser'].parse(rule['Value'])
        return d


class SnapshotParser(Parser):
    """the Parser to parse a quote snapshot"""

    def __init__(self, exchange, protocol):
        super(SnapshotParser, self).__init__(exchange, protocol)
        self._exchange_id = exchange

    def parse(self, msg):
        pass
