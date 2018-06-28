#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import requests
import urllib
import urllib2
import re
import cookielib
import json
import configparser
import util
from BeautifulSoup import BeautifulSoup as BS

jar = cookielib.FileCookieJar("cookie")
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))

config = configparser.ConfigParser()
config.read('config.cfg')

api_url = config['api']['url']
token = ''

def get_asocioj():
    util.ensaluti(opener)
    data_listo = urllib.urlencode({
        "lando":"ne+indikita",
        "jaro": "2018",
        "ekskl": "jes",
        "listoj": "",
        "listo": "listig",
        "uea_kodo": "j",
        "nomo": "j",
        "regno": "j",
        "mem": "j",
        "viv": "jes",
        "la_a": "jes",
        "la_n": "jes",
        "ls_n": "jes",
        "fa_a": "jes",
        "fa_k": "jes",
        "fa_n": "jes",
        "fs_a": "jes",
        "lg": "jes",
        "lk": "jes",
        "lista_nomo": "listig"
    })
    url = 'https://db.uea.org/index.php?listo=listig'
    list_request = urllib2.Request(url, data_listo)
    opener.addheaders = [('Referer', 'https://db.uea.org/index.php?listo=listig')]
    list_reply = opener.open(list_request)
    return list_reply.read()

arq = open("browser.html", "w")
arq.write(get_asocioj())
arq.close()