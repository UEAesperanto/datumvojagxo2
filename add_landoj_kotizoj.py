#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import requests
import urllib
import urllib2
import json
from BeautifulSoup import BeautifulSoup as BS

config = configparser.ConfigParser()
config.read('config.cfg')

api_url = config['api']['url']
token = ''

def get_token():
    if(token == ''):
        data = {'uzantnomo': config['api']['uzantnomo'], 'pasvorto': config['api']['pasvorto']}
        response = requests.post(api_url + '/admin/ensaluti', data=data)
        return response.json()['token']
    else:
        return token

def get_config(valoro):
    url = api_url + "/config/" + valoro
    response = requests.get(url)
    return str(response.json()[valoro])

def insert_kategorioj():
    id_juna = get_config("idJunajGrupoj")
    headers = {'x-access-token': get_token()}

    for data in kategorioj:
        request = requests.post(api_url + '/grupoj', headers=headers, data=data)

        if(request.status_code == 403):
            token = ''
            headers = {'x-access-token': get_token()}
            request = requests.post(api_url + '/grupoj', headers=headers, data=data)

        if('insertId' in request.json()):
            id_grupo = str(request.json()['insertId'])
            data['id'] = id_grupo

            if(data['tipo']):
                url = api_url + '/grupoj/kategorioj/' + data['tipo'] + '/sub/' + id_grupo
                requests.post(url, headers=headers)

            if(data['juna']):
                url = api_url + '/grupoj/kategorioj/' + id_juna + '/sub/' + id_grupo
                requests.post(url, headers=headers)

def insert_lando(lando):
    radikoEO = lando.img['title']
    landkodo = lando.img['src'].replace('.png', '').split('/')[3]
    valuto = lando.contents[4].text

    data = {'radikoEo': radikoEO, 'finajxoEo': '', 'landkodo': landkodo, 'valuto': valuto}
    headers = {'x-access-token': get_token()}
    request = requests.post(api_url + '/landoj', headers=headers, data=data)
    if(request.status_code == 403):
        token = ''
        headers = {'x-access-token': get_token()}
        request = requests.post(api_url + '/landoj', headers=headers, data=data)

    return request.json()['insertId']

def insert_kotizo(id_lando, kotizo, id_grupo):
    if('id' in id_grupo):
        id_grupo = id_grupo['id']
        data = {'idLando':id_lando, 'prezo': kotizo, 'junaRabato': 0}
        headers = {'x-access-token': get_token()}
        request = requests.post(api_url + "/grupoj/" + id_grupo + "/kotizoj", headers=headers, data=data)

def get_landoj_kotizoj():
    url = 'https://uea.org/alighoj/kotiztabelo'
    request = urllib2.Request(url)
    opener = urllib2.build_opener()
    reply = opener.open(request)
    soup = BS(reply.read())
    landoj_kotizoj = soup.findAll('tr')

    for lando in landoj_kotizoj[1:]:
        print "Enmetas nun informojn pri: " + lando.text
        id_lando = insert_lando(lando.contents[0])
        insert_kotizo(id_lando, int(lando.contents[1].text) * 100, kategorioj[0])
        insert_kotizo(id_lando, int(lando.contents[2].text) * 100, kategorioj[1])
        insert_kotizo(id_lando, int(lando.contents[3].text) * 100, kategorioj[2])
        insert_kotizo(id_lando, int(lando.contents[5].text) * 100, kategorioj[5])
        insert_kotizo(id_lando, int(lando.contents[6].text) * 100, kategorioj[3])
        insert_kotizo(id_lando, int(lando.contents[7].text) * 100, kategorioj[4])

id_membrecgrupo = get_config("idMembrecgrupo")
id_aldonamembreco = get_config("idAldonaMembrecgrupo")
kategorioj = [
              {
                'mallongigilo': 'MG',
                'id': '23',
                'nomo': 'Membro kun Gvidlibro',
                'priskribo': 'Individua membro, kiu ricevas nur la Gvidlibron\
                             tra la Esperanto-movado plus la revuon Esperanto rete.',
                'tipo': id_membrecgrupo,
                'juna': False
               },
               {
                 'mallongigilo': 'MJ',
                 'id': '24',
                 'nomo': 'Membro kun Jarlibro',
                 'priskribo': 'Individua membro, kiu ricevas la Jarlibron plus \
                              retan version de la revuo Esperanto.',
                 'tipo': id_membrecgrupo,
                 'juna': False
               },
               {
                 'mallongigilo': 'MA',
                 'id': '25',
                 'nomo': 'Membro Abonanto',
                 'priskribo': 'Individua membro, kiu ricevas la Jarlibron kaj \
                              la revuon Esperanto.',
                 'tipo': id_membrecgrupo,
                 'juna': False
               },
               {
                 'mallongigilo': 'SZ',
                 'id': '26',
                 'nomo': 'Societo Zamenhof',
                 'priskribo': 'Membro de Societo Zamenhof, kiu volas \
                               finance apogi Universalan Esperanto-Asocion. ',
                 'tipo': id_aldonamembreco,
                 'juna': False
               },
               {
                 'mallongigilo': 'PT',
                 'id': '27',
                 'nomo': 'Patrono de TEJO',
                 'priskribo': 'Patrono de TEJO, kiu ricevas la eldonaĵojn de TEJO. ',
                 'tipo': id_aldonamembreco,
                 'juna': True
               },
               {
                'mallongigilo': 'KTO',
                'id': '28',
                'nomo': 'Abono al la revuo Kontakto',
                'priskribo': 'Se vi estas en TEJO aĝo (ĝis 35 jarojn), aliĝante kiel Membro Abonanto\
                              aŭ Membro kun Jarlibro, vi JAM ricevos abonon de revuo Kontakto',
                'tipo': id_aldonamembreco,
                'juna': True
               },
               {
                'mallongigilo': 'HM',
                'nomo': 'Honora Membro',
                'priskribo': 'esperantistoj, kiuj faris gravajn servojn al la tutmonda Esperanto-movado.',
                'tipo': None,
                'juna': True
               }
            ]

insert_kategorioj()
get_landoj_kotizoj()
