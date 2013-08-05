#-*- coding: utf-8 -*-

import re

JS_ESCAPE_MAP = {
    '\\'     : '\\\\',
    '</'     : '<\/',
    "\r\n"   : '\n',
    "\n"     : '\n',
    "\r"     : '\n',
    '"'      : '\\"',
    "'"      : "\\'",
    "'"      : "\\'",
    "'"      : "\\'",
    '\u2028' : '&#x2028;',
    '\u2029' : '&#x2029;'
    }
 	
def escapejs(s):
    p = r'''(\|<\/|\r\n|\342\200\250|\342\200\251|[\n\r"'])'''
    r = lambda m: JS_ESCAPE_MAP.get(m.group())
    return s and re.sub(p, r, s, flags=re.I|re.M|re.X) or ''


def dateformat(value, format="%Y-%m-%d %H:%M:%S"):
    return value.strftime(format)

