# -*- coding: utf-8 -*-

from parsers.parsers import ParserDemo


def test_board():
    parser = ParserDemo(5)
    assert parser.getNum() == 5
