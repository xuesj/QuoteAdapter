# -*- coding: utf-8 -*-
# Update Description
# @2016/4/26, Created by Xuesj

from parsers.parsers import Parser


def test_board():
    parser = Parser(5)
    assert parser.getNum() == 5
