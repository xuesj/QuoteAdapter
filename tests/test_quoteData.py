# -*- coding: UTF-8 -*-
from collections import defaultdict
from parsers.Parsers import StringParser, IntParser, DatetimeParser, LineParser
from utils import Exchange, Protocol
from parsers.Quotes import QuoteSnapshot


def test_head_rule_file():

    rule_file = '../parsers/head_rule.conf'
    ex = Exchange.SH
    protocol = Protocol.FILE
    line_type = LineParser.HEAD
    head_parser = LineParser(ex, protocol, rule_file, line_type)

    assert head_parser.parse_rules[0]['Seq'] == '1'
    assert head_parser.parse_rules[1]['Seq'] == '2'
    assert head_parser.parse_rules[2]['Seq'] == '3'
    assert head_parser.parse_rules[3]['Seq'] == '4'
    assert head_parser.parse_rules[4]['Seq'] == '5'
    assert head_parser.parse_rules[5]['Seq'] == '6'
    assert head_parser.parse_rules[6]['Seq'] == '7'
    assert head_parser.parse_rules[7]['Seq'] == '8'
    assert head_parser.parse_rules[8]['Seq'] == '9'

    d = defaultdict(dict)
    d['Seq'] = '1'
    d['Name'] = 'BeginString'
    d['Desc'] = 'Start identify'
    d['Rule_String'] = 'C6'
    d['Value'] = 'HEADER'

    assert head_parser.parse_rules[0]['Seq'] == d['Seq']
    assert head_parser.parse_rules[0]['Name'] == d['Name']
    assert head_parser.parse_rules[0]['Desc'] == d['Desc']
    assert head_parser.parse_rules[0]['Rule_String'] == d['Rule_String']
    assert head_parser.parse_rules[0]['Value'] == d['Value']
    assert isinstance(head_parser.parse_rules[0]['Parser'], StringParser)
    assert isinstance(head_parser.parse_rules[1]['Parser'], StringParser)
    assert isinstance(head_parser.parse_rules[2]['Parser'], IntParser)
    assert isinstance(head_parser.parse_rules[3]['Parser'], IntParser)
    assert isinstance(head_parser.parse_rules[4]['Parser'], IntParser)
    assert isinstance(head_parser.parse_rules[5]['Parser'], StringParser)
    assert isinstance(head_parser.parse_rules[6]['Parser'], DatetimeParser)
    assert isinstance(head_parser.parse_rules[7]['Parser'], IntParser)
    assert isinstance(head_parser.parse_rules[8]['Parser'], StringParser)

    assert head_parser.parse_rules[0]['Value'] == 'HEADER'
    assert head_parser.parse_rules[1]['Value'] == 'MTP1.00'
    assert head_parser.parse_rules[2]['Value'] is ''
    assert head_parser.parse_rules[3]['Value'] is ''
    assert head_parser.parse_rules[4]['Value'] is ''
    assert head_parser.parse_rules[5]['Value'] is ''
    assert head_parser.parse_rules[6]['Value'] is ''
    assert head_parser.parse_rules[7]['Value'] == '0'
    assert head_parser.parse_rules[8]['Value'] is ''
