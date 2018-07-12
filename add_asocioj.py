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

def post_uzanto(uzanto_json):
    headers = {'x-access-token': util.get_token(token)}
    request = requests.post(api_url + '/uzantoj/adapti', headers=headers, data=uzanto_json)
    if request.status_code == 201:
        return  request.json()['id']
    elif request.status_code == 200:
        print request.json()[0]['id']
        return request.json()[0]['id']
    else:
        print request.status_code, uzanto_json
        return -1


def post_membrecoj(data):
    headers = {'x-access-token': util.get_token(token)}
    url = api_url + '/grupoj/' + str(data['idGrupo']) + '/anoj'
    request = requests.post(url, headers=headers, json=data)
    if request.status_code != 201:
        print url, data, request.status_code


def get_membrecoj(membrecoj_str):
    membrecoj = []
    for membreco in membrecoj_str:
        membreco = membreco.replace(' ', '')
        if 'la.a' == membreco:
            membrecoj.append({'idGrupo':grupoj['LA.A'],
                              'komencdato':'2018-01-01',
                              'findato': None,
                              'dumviva': 1})
        elif 'ls.a' == membreco:
            membrecoj.append({'idGrupo':grupoj['LS.A'],
                              'komencdato':'2018-01-01',
                              'findato': None,
                              'dumviva': 1})
        elif 'ls.n' == membreco:
            membrecoj.append({'idGrupo':grupoj['LS.N'],
                              'komencdato':'2018-01-01',
                              'findato': None,
                              'dumviva': 1})
        elif 'fa.a' == membreco:
            membrecoj.append({'idGrupo':grupoj['FA.A'],
                              'komencdato':'2018-01-01',
                              'findato': None,
                              'dumviva': 1})
        elif 'fa.k' == membreco:
            membrecoj.append({'idGrupo':grupoj['FA.K'],
                              'komencdato':'2018-01-01',
                              'findato': None,
                              'dumviva': 1})
        elif 'fa.n' == membreco:
            membrecoj.append({'idGrupo':grupoj['FA.N'],
                              'komencdato':'2018-01-01',
                              'findato': None,
                              'dumviva': 1})
        elif 'fs.n' == membreco:
            membrecoj.append({'idGrupo':grupoj['FS.N'],
                              'komencdato':'2018-01-01',
                              'findato': None,
                              'dumviva': 1})
        elif 'lg' == membreco:
            membrecoj.append({'idGrupo':grupoj['LG'],
                              'komencdato':'2018-01-01',
                              'findato': None,
                              'dumviva': 1})
        elif 'lk' == membreco:
            membrecoj.append({'idGrupo':grupoj['LK'],
                              'komencdato':'2018-01-01',
                              'findato': None,
                              'dumviva': 1})
    return membrecoj

def get_asocioj():
    util.ensaluti(opener)
    data_listo = urllib.urlencode({
        "adreso":"j",
        "lando":"ne+indikita",
        "jaro": "2018",
        "ekskl": "jes",
        "listoj": "",
        "listo": "listig",
        "uea_kodo": "j",
        "nomo": "j",
        "regno": "j",
        "mem": "j",
        "ndat": "j",
        "nomo": "j",
        "pkodo": "j",
        "regno": "j",
        "urbo":"j",
        "ret":"j",
        "lista_nomo": "listig",
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
    })
    url = 'https://db.uea.org/index.php?listo=listig'
    list_request = urllib2.Request(url, data_listo)
    opener.addheaders = [('Referer', 'https://db.uea.org/index.php?listo=listig')]
    list_reply = opener.open(list_request)
    return list_reply.read()

def get_landoj():
    response = requests.get(api_url + '/landoj')
    return dict(map(lambda x: [x['landkodo'], x['id']], response.json()))

def get_grupoj():
    response = requests.get(api_url + '/grupoj')
    return dict(map(lambda x: [x['mallongigilo'], x['id']], response.json()))

def krei_uzanton(uzanto):
    # prenas uea-kodo
    ueakodo = uzanto[0].text.replace('&nbsp;', '')

    # Ligilo al informplena paĝo
    pagxligilo = uzanto[0].a['href']
    url = 'https://db.uea.org' + pagxligilo

    try:
        uzanto_request = urllib2.Request(url)
        uzanto_reply = opener.open(uzanto_request)
        soup_pagxo = BS(uzanto_reply.read())
    except Exception as e:
        print url
        pass

    # prenas persona nomo
    personaj_nomoj = uzanto[1].contents[0].split(' ')
    persona_nomo = ' '.join(personaj_nomoj)

    # prenas familianomo
    familia_nomo = uzanto[1].contents[1].text

    # prenas adreso
    adreso = uzanto[2].text.replace('&nbsp;', '')

    #prenas urbo
    urbo = uzanto[3].text.replace('&nbsp;', '')

    #prenas posxtkodo
    posxtkodo = uzanto[4].text.replace('&nbsp;', '')

    try:
       #prenas idLando
       id_lando = landoj[uzanto[5].img['alt']]
    except:
       id_lando = -1

    #prenas retadreso
    retadreso = uzanto[6].text.replace('&nbsp;', '')

    #prenas naskigxtago
    naskigxtago = uzanto[7].text.replace('&nbsp;', '').replace('00', '01').replace('/','-')
    if naskigxtago == '':
        naskigxtago = '1859-12-15'

    try:
       hejma_telefono = soup_pagxo.find(text='Hejma telefono').parent.nextSibling.text.replace('&nbsp;', '')
    except Exception as e:
       hejma_telefono = ''
       pass

    try:
       notoj = soup_pagxo.find(text='Notoj').parent.nextSibling.text.replace('&nbsp;', '')
    except Exception as e:
       notoj = ''
       pass

    try:
       telportebla  = soup_pagxo.find(text='Poŝtelefono').parent.nextSibling.text.replace('&nbsp;', '')
    except Exception as e:
       telportebla = ''
       pass

    try:
       ueakodo = soup_pagxo.find(text='UEA-kodo').parent.nextSibling.text.replace('&nbsp;', '').replace('-', '')
    except Exception as e:
       ueakodo = ''
       pass

    id_faktemoj =[]
    try:
        del_faktemoj = soup_pagxo.find(text='Delegita fako').parent.nextSibling.text.replace('&nbsp;', '').split("\n")
        for faktemo in del_faktemoj:
            id_faktemoj.append(add_faktemo(faktemo))
    except Exception as e:
       pass

    try:
        konst_kat = soup_pagxo.find(text='Konst. kat.').parent.nextSibling.text.replace('&nbsp;', '').split(', ')
        membrecoj = get_membrecoj(konst_kat)
    except Exception as e:
        membrecoj = []
        pass

    uzanto_json = {'ueakodo': ueakodo,
                   'titolo': '',
                   'personanomo': persona_nomo,
                   'familianomo': familia_nomo,
                   'adreso': adreso,
                   'urbo': urbo,
                   'telhejmo': hejma_telefono,
                   'telportebla': telportebla,
                   'posxtkodo': posxtkodo,
                   'idLando': id_lando,
                   'retposxto': retadreso,
                   'naskigxtago': naskigxtago,
                   'notoj': notoj,
                   'membrecoj': membrecoj}
    if (len(membrecoj) != 0):
        id_ano = post_uzanto(uzanto_json)
        if (id_ano != -1) and (id_ano is not None):
            for membreco in membrecoj:
                membreco['idAno'] = id_ano
                post_membrecoj(membreco)
        else:
            ne_funkciis = open("ne_funkciis.txt", "a")
            ne_funkciis.write("\nUzanto: " + str(uzanto_json) + "\n")
            ne_funkciis.close()

landoj = get_landoj()
asocioj_reply = get_asocioj()
grupoj = get_grupoj()

soup = BS(asocioj_reply)
asocioj = soup.findAll('tr')
asocioj = asocioj[2:len(asocioj)]

for asocio in asocioj:
    try:
        soup1 = BS(str(asocio))
        asocio = soup1.findAll('td')
        krei_uzanton(asocio)
    except Exception as e:
        print asocio
        print e


