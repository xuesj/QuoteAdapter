# -*- coding: UTF-8 -*-
import abc
from collections import defaultdict
import datetime


class Parser(object):
    """Abstract Class of Parser"""
    PADDING_LEFT = 0
    PADDING_RIGHT = 1

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self._parse_rules = defaultdict(dict)

    @abc.abstractmethod
    def parse(self, msg):
        pass

    @classmethod
    def get_field_parser(cls, parse_rule):
        field_parsers = {
            'C': StringParser,
            'N': IntParser,
            'F': FloatParser,
            'D': DatetimeParser,
            'T': TimeParser
        }
        leading = parse_rule[0]
        return field_parsers[leading](parse_rule)


class StringParser(Parser):
    def __init__(self, parse_rule):
        super(StringParser, self).__init__()
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
    def __init__(self, parse_rule):
        super(IntParser, self).__init__()
        leading, msg_len = parse_rule[0], int(parse_rule[1:])
        assert leading == 'N'
        assert isinstance(msg_len, int)
        self._parse_rules['leading'] = leading
        self._parse_rules['length'] = msg_len
        self._parse_rules['padding'] = Parser.PADDING_LEFT
        self._parse_rules['desc'] = 'NX: space padding left'

    def parse(self, msg):
        if self._parse_rules['padding'] == Parser.PADDING_RIGHT:
            return int(msg[:self._parse_rules['length']])
        elif self._parse_rules['padding'] == Parser.PADDING_LEFT:
            return int(msg[-self._parse_rules['length']:])
        else:
            raise TypeError


class FloatParser(Parser):
    def __init__(self, parse_rule):
        super(FloatParser, self).__init__()
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
        self._parse_rules['desc'] = 'NX(Y): space padding left'

    def parse(self, msg):
        f = float(msg)
        assert isinstance(f, float)
        return f


class DatetimeParser(Parser):
    def __init__(self, parse_rule):
        super(DatetimeParser, self).__init__()
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
    def __init__(self, parse_rule):
        super(TimeParser, self).__init__()
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


class SnapshotParser(Parser):
    """the Parser to parse a quote snapshot"""

    def __init__(self, exchange_id):
        super(SnapshotParser, self).__init__()
        self._exchange_id = exchange_id

    def parse(self, msg):
        pass
