# -*- coding: utf-8 -*-

"""Translate text using Google Translate.
Usage: tr <src lang> <dest lang> <text>
Example: tr en fr hello

Check available languages here: https://cloud.google.com/translate/docs/languages"""

import json
import requests
import os
from lxml.html import fromstring
from uuid import uuid4

from albertv0 import *

__iid__ = "PythonInterface/v0.1"
__prettyname__ = "金山词霸"
__version__ = "1.0"
__trigger__ = "dict "
__author__ = "Apuyuseng"
__dependencies__ = []

ua = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.3202.62 Safari/537.36"

iconPath = os.path.dirname(__file__)+"/dict.ico"
if not os.path.isfile(iconPath):
    iconPath = ":python_module"


def handleQuery(query):
    if query.isTriggered:
        search = query.string.strip()
        link = 'http://www.iciba.com/word?w=%s'%search
        if search:
            resp = requests.get(link, headers={'User-Agent': ua})
            root = fromstring(resp.text)
            ret = []
            if root.xpath('//ul[starts-with(@class,"Mean_part")]/li/i'):
                keys = root.xpath('//ul[starts-with(@class,"Mean_symbols")]/li/text()')
                key = ' '.join(keys)
                values = root.xpath('//ul[starts-with(@class,"Mean_part")]/li/i/text()|//ul[starts-with(@class,"Mean_part")]/li/div/span/text()')
                value =  ' '.join(values)
                return Item(id=__prettyname__+uuid4().hex,
                                icon=iconPath, 
                                completion=query.rawString,
                                text=key,
                                subtext=value,
                                actions=[ClipAction("Copy translation to clipboard", key)]
                                )
            else:
                for node in root.xpath('//ul[starts-with(@class,"Mean_part")]/li'):
                    key = node.xpath('./span/text()')[0].strip()
                    value = ''.join(node.xpath('./div/span/text()'))
                    ret.append(Item(id=__prettyname__+uuid4().hex,
                                icon=iconPath, 
                                completion=query.rawString,
                                text=key,
                                subtext=value,
                                actions=[ClipAction("Copy translation to clipboard", key)]
                                ))
                
                return ret
        else:
            item = Item(id=__prettyname__, icon=iconPath, completion=query.rawString)
            item.text = __prettyname__
            item.subtext = "请输入搜索词"
            return item
