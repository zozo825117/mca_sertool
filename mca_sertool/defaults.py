#! /usr/bin/env python
#  -*- coding: utf-8 -*-

from keymaps import *

defaults = {'serial_port': '',
            'baudrate': '115200',
            'parity': '',
            'bytesize': '',
            'stopbits': '',
            'rec_hex_ascii': 0,
            'linefeed': 0,
            'linefeedtime': 0,
            'id_type': 'dec',
            'rec_count': 0,
            # '帧格式': 'ID:4BXXXXXXXX',
            '帧格式': 'a9 00 00 00 00 00 00 00 |xx xx xx xx xx xx kk rr',
            '帧长': '',
            DEF_CHECK: 'None',
            '效验格式': 'a9 00 00 00 00 00 00 00 |xx xx xx xx xx xx',
            'id': '05a66c000001-05a66c000010|05a66c000101',
            DEF_TOTAL_ID_NUM: 0,
            DEF_INVALID_ID_NUM: 0,
            DEF_AVAILABLE_ID_NUM: 0,
            }
