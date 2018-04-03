#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import requests
import urllib
import urllib2
import re
import cookielib
import json
import configparser
from BeautifulSoup import BeautifulSoup as BS

jar = cookielib.FileCookieJar("cookie")
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))

config = configparser.ConfigParser()
config.read('config.cfg')

api_url = config['api']['url']
token = ''

def ensaluti():
    url = 'https://db.uea.org/index.php'
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'

    data_login = urllib.urlencode(
                 {"uvorto": config['nuna_db']['uzantnomo'],
                 "pvorto": config['nuna_db']['pasvorto']})
    login_request = urllib2.Request(url, data_login)
    opener.open(login_request)

def get_token():
    if(token == ''):
        data = {'uzantnomo': config['api']['uzantnomo'], 'pasvorto': config['api']['pasvorto']}
        response = requests.post(api_url + '/admin/ensaluti', data=data)
        return response.json()['token']
    else:
        return token

def post_uzanto(uzanto_json):
    headers = {'x-access-token': get_token()}
    request = requests.post(api_url + '/uzantoj/adapti', headers=headers, data=uzanto_json)
    if request.status_code == 201:
        return request.json()['id']
    elif request.status_code == 200:
        print request.json()
    else:
        print request.status_code, uzanto_json
        return -1

def get_landoj():
    response = requests.get(api_url + '/landoj')
    return dict(map(lambda x: [x['landkodo'], x['id']], response.json()))

def get_grupoj():
    response = requests.get(api_url + '/grupoj')
    return dict(map(lambda x: [x['mallongigilo'], x['id']], response.json()))

def get_membroj():
    ensaluti()
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

def get_membrecoj(membrecoj_str):
    membrecoj = []
    for membreco in membrecoj_str:
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
    return membrecoj

def post_membrecoj(data):
    headers = {'x-access-token': get_token()}
    url = api_url + '/grupoj/' + str(data['idGrupo']) + '/anoj'
    request = requests.post(url, headers=headers, json=data)
    if request.status_code != 201:
        print url, data, request.status_code

def krei_uzanton(uzanto):
    # prenas uea-kodo
    ueakodo = uzanto[0].text.replace('&nbsp;', '')

    # prenas titolo
    titoloj = ['S-ro', 'S-ino', 'Mag.', 'D-ro', 'D-ino', 'Pastro', 'Pastrino', 'F-ino']
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

    uzanto_json = {'ueakodo': ueakodo,
                   'titolo': titolo,
                   'personanomo': persona_nomo,
                   'familianomo': familia_nomo,
                   'adreso': adreso,
                   'urbo': urbo,
                   'posxtkodo': posxtkodo,
                   'idLando': id_lando,
                   'retposxto': retadreso,
                   'naskigxtago': naskigxtago,
                   'membrecoj': membrecoj}

    if (len(membrecoj) != 0):
        id_ano = post_uzanto(uzanto_json)
        if(id_ano != -1) and (id_ano is not None):
            for membreco in membrecoj:
                membreco['idAno'] = id_ano
                post_membrecoj(membreco)

landoj = get_landoj()
grupoj = get_grupoj()
reply_data_listo = get_membroj()
soup = BS(reply_data_listo)

uzantoj = soup.findAll('tr')
uzantoj = uzantoj[2:len(uzantoj)]

for uzanto in uzantoj:
    soup = BS(str(uzanto))
    uzanto = soup.findAll('td')
    krei_uzanton(uzanto)
