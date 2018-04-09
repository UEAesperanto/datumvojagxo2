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
        return request.json()['id']
    else:
        print request.status_code, uzanto_json
        return -1

def get_landoj():
    response = requests.get(api_url + '/landoj')
    return dict(map(lambda x: [x['landkodo'], x['id']], response.json()))

def get_fakoj():
    response = requests.get(api_url + '/faktemoj')
    return dict(map(lambda x: [x['nomo'], x['id']], response.json()))

def get_grupoj():
    response = requests.get(api_url + '/grupoj')
    return dict(map(lambda x: [x['mallongigilo'], x['id']], response.json()))

def get_membroj():
    util.ensaluti(opener)
    data_listo = urllib.urlencode(
                 {"adreso":"j",
                 "ekskl":"jes",
                 "jaro":"2018",
                 "kelkaj":"uea_membraro",
                 "lando":"ne indikita",
                 "lista_nomo":"listig",
                 "listoj": "",
                 "mem": "j",
                 "ndat": "j",
                 "nomo": "j",
                 "pkodo": "j",
                 "regno": "j",
                 "ret":"j",
                 "uea_kodo":"j",
                 "urbo":"j",
                 "viv":"jes"})
    url = 'https://db.uea.org/index.php?listo=listig'
    list_request = urllib2.Request(url, data_listo)
    opener.addheaders = [('Referer', 'https://db.uea.org/index.php?listo=listig')]
    list_reply = opener.open(list_request)
    return list_reply.read()

def get_membrecoj(membrecoj_str, **kwargs):
    membrecoj = []
    for membreco in membrecoj_str:
        membreco = membreco.replace(' ', '')
        if ('ma201' in membreco) or ('mat201' in membreco):
            length = len(membreco)
            jarcifero = int(membreco[length - 2 : length])
            membrecoj.append({'idGrupo':grupoj['MA'],
                              'komencdato':'20' + str(jarcifero) + '-01-01',
                              'findato': '20' + str(jarcifero + 1) + '-02-20',
                              'dumviva': 0})
        elif ('dm' == membreco) or ('dmt' == membreco):
            membrecoj.append({'idGrupo':grupoj['MA'],
                              'komencdato':'2018-01-01',
                              'findato': None,
                              'dumviva': 1})
        elif ('hm' == membreco) :
            membrecoj.append({'idGrupo':grupoj['MA'],
                              'komencdato':'2018-01-01',
                              'findato': None,
                              'dumviva': 1})
            membrecoj.append({'idGrupo':grupoj['HM'],
                              'komencdato':'2018-01-01',
                              'findato': None,
                              'dumviva': 1})
        elif ('mj201' in membreco) or ('mjt201' in membreco):
            length = len(membreco)
            jarcifero = int(membreco[length - 2 : length])
            membrecoj.append({'idGrupo':grupoj['MJ'],
                              'komencdato':'20' + str(jarcifero) + '-01-01',
                              'findato': '20' + str(jarcifero + 1) + '-02-20',
                              'dumviva': 0})
        elif ('dmj' == membreco) or ('dmjt' == membreco):
            membrecoj.append({'idGrupo':grupoj['MJ'],
                              'komencdato':'2018-01-01',
                              'findato': None,
                              'dumviva': 1})
        elif ('kto' in membreco):
            length = len(membreco)
            jarcifero = int(membreco[length - 2 : length])
            membrecoj.append({'idGrupo':grupoj['KTO'],
                              'komencdato':'20' + str(jarcifero) + '-01-01',
                              'findato': '20' + str(jarcifero + 1) + '-02-20',
                              'dumviva': 0})
        elif ('dpt' == membreco):
            membrecoj.append({'idGrupo':grupoj['PT'],
                              'komencdato':'2018-01-01',
                              'findato': None,
                              'dumviva': 1})
        elif ('mg' in membreco):
            length = len(membreco)
            jarcifero = int(membreco[length - 2 : length])
            membrecoj.append({'idGrupo':grupoj['MG'],
                              'komencdato':'20' + str(jarcifero) + '-01-01',
                              'findato': '20' + str(jarcifero + 1) + '-02-20',
                              'dumviva': 0})
        elif ('pt' in membreco):
            length = len(membreco)
            jarcifero = int(membreco[length - 2 : length])
            membrecoj.append({'idGrupo':grupoj['PT'],
                              'komencdato':'20' + str(jarcifero) + '-01-01',
                              'findato': '20' + str(jarcifero + 1) + '-02-20',
                              'dumviva': 0})
        elif ('sz' in membreco):
            length = len(membreco)
            jarcifero = int(membreco[length - 2 : length])
            membrecoj.append({'idGrupo':grupoj['SZ'],
                              'komencdato':'20' + str(jarcifero) + '-01-01',
                              'findato': '20' + str(jarcifero + 1) + '-02-20',
                              'dumviva': 0})
        elif ('es' == membreco):
            membrecoj.append({'idGrupo':grupoj['ES'],
                              'komencdato':'2018-01-01',
                              'findato': None,
                              'dumviva': 1})
        elif ('kom.a' == membreco):
            membrecoj.append({'idGrupo':grupoj['KOM.A'],
                              'komencdato':'2018-01-01',
                              'findato': None,
                              'dumviva': 1})
        elif ('kom.b' == membreco):
            membrecoj.append({'idGrupo':grupoj['KOM.B'],
                              'komencdato':'2018-01-01',
                              'findato': None,
                              'dumviva': 1})
        elif ('kom.c' == membreco):
            membrecoj.append({'idGrupo':grupoj['KOM.C'],
                              'komencdato':'2018-01-01',
                              'findato': None,
                              'dumviva': 1})
        elif ('d' == membreco):
            membrecoj.append({'idGrupo':grupoj['d'],
                              'komencdato':'2018-01-01',
                              'findato': None,
                              'dumviva': 1})
        elif ('fd' == membreco):
            id_faktemoj = kwargs['id_faktemoj']
            print id_faktemoj
            membrecoj.append({'idGrupo':grupoj['fd'],
                              'komencdato':'2018-01-01',
                              'faktemoj': id_faktemoj,
                              'findato': None,
                              'dumviva': 1})
        elif ('vd' == membreco):
            membrecoj.append({'idGrupo':grupoj['vd'],
                              'komencdato':'2018-01-01',
                              'findato': None,
                              'dumviva': 1})
        elif ('jd' == membreco):
            membrecoj.append({'idGrupo':grupoj['jd'],
                              'komencdato':'2018-01-01',
                              'findato': None,
                              'dumviva': 1})
    return membrecoj

def post_membrecoj(data):
    headers = {'x-access-token': util.get_token(token)}
    url = api_url + '/grupoj/' + str(data['idGrupo']) + '/anoj'
    request = requests.post(url, headers=headers, json=data)
    if request.status_code != 201:
        print url, data, request.status_code

def add_faktemo(faktemo):
    if faktemo in fakoj:
        return fakoj[faktemo]
    else:
        headers = {'x-access-token': util.get_token(token)}
        url = api_url + '/faktemoj'
        data = {'nomo': faktemo, 'priskribo': ''}
        request = requests.post(url, headers=headers, json=data)
        fakoj[faktemo] = request.json()['insertId']
        return request.json()['insertId']

def krei_uzanton(uzanto):
    # prenas uea-kodo
    pagxligilo = uzanto[0].a['href']
    url = 'https://db.uea.org' + pagxligilo

    try:
        uzanto_request = urllib2.Request(url)
        uzanto_reply = opener.open(uzanto_request)
        soup_pagxo = BS(uzanto_reply.read())
    except Exception as e:
        print url
        pass

    # prenas titolo
    titoloj = ['S-ro', 'S-ino', 'Mag.', 'D-ro', 'D-ino', 'Pastro', 'Pastrino',
               'F-ino', 'Prof. D-ro', 'Prof-ino', 'Prof.']
    ebla_titolo = uzanto[1].contents[0].split(' ')[0]
    if ebla_titolo in titoloj:
        titolo = ebla_titolo
    else:
        titolo = ''

    # prenas persona nomo
    personaj_nomoj = uzanto[1].contents[0].split(' ')
    if titolo != '':
        personaj_nomoj = personaj_nomoj[1:len(personaj_nomoj)]
    persona_nomo = ' '.join(personaj_nomoj)

    # prenas familianomo
    familia_nomo = uzanto[1].contents[1].text

    # prenas adreso
    adreso = uzanto[2].text.replace('&nbsp;', '')

    #prenas urbo
    urbo = uzanto[3].text.replace('&nbsp;', '')

    #prenas posxtkodo
    posxtkodo = uzanto[4].text.replace('&nbsp;', '')

    #prenas idLando
    id_lando = landoj[uzanto[5].img['alt']]

    #prenas retadreso
    retadreso = uzanto[6].text.replace('&nbsp;', '')

    #prenas naskigxtago
    naskigxtago = uzanto[7].text.replace('&nbsp;', '').replace('/','-')

    #prenas membrecoj
    membrecoj = uzanto[8].text.replace('&nbsp;', '').replace(' ', '').split(',')
    membrecoj = get_membrecoj(membrecoj)

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
        konst_kat = get_membrecoj(konst_kat, id_faktemoj = id_faktemoj)
        membrecoj = membrecoj + konst_kat
    except Exception as e:
       pass

    uzanto_json = {'ueakodo': ueakodo,
                   'titolo': titolo,
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
grupoj = get_grupoj()
fakoj = get_fakoj()
reply_data_listo = get_membroj()
soup = BS(reply_data_listo)
uzantoj = soup.findAll('tr')
uzantoj = uzantoj[2:len(uzantoj)]

for i in range(len(uzantoj)):
    try:
        soup = BS(str(uzantoj[i]))
        uzanto = soup.findAll('td')
        krei_uzanton(uzanto)
    except Exception as e:
        homo1 = open("homo1.html", "w")
        homo1.write(str(i) + str(uzanto))
        homo1.close()
        raise e
