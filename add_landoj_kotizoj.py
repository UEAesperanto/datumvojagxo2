#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import requests
import urllib
import urllib2
import json
import configparser
import util
from BeautifulSoup import BeautifulSoup as BS

config = configparser.ConfigParser()
config.read('config.cfg')

api_url = config['api']['url']

def get_kategorioj():
    response = requests.get(api_url + '/grupoj')
    return dict(map(lambda x: [x['mallongigilo'], x['id']], response.json()))


def insert_lando(lando, token):
    radikoEO = lando.img['title']
    landkodo = lando.img['src'].replace('.png', '').split('/')[3]
    valuto = lando.contents[4].text

    response = requests.get(api_url + '/landoj?landkodo=' + landkodo)
    if 'id' in response.json()[0]:
        print response.json()[0]['id']
        return response.json()[0]['id']

    data = {'radikoEo': radikoEO, 'finajxoEo': '', 'landkodo': landkodo, 'valuto': valuto}
    token = util.get_token(token)
    headers = {'x-access-token': token}
    request = requests.post(api_url + '/landoj', headers=headers, data=data)

    if (request.status_code == 400) or (request.status_code == 403):
        token = ''
        token = util.get_token(token)
        headers = {'x-access-token': token}
        request = requests.post(api_url + '/landoj', headers=headers, data=data)

    return request.json()['insertId']

def insert_kotizo(id_lando, kotizo, id_grupo, token):
    if(id_grupo):
        data = {'idLando':id_lando, 'prezo': kotizo, 'junaRabato': 0}
        token = util.get_token(token)
        headers = {'x-access-token': token}
        request = requests.post(api_url + "/grupoj/" + str(id_grupo) + "/kotizoj", headers=headers, data=data)
        if (request.status_code == 400) or (request.status_code == 403):
            token = ''
            token = util.get_token(token)
            headers = {'x-access-token': token}
            request = requests.post(api_url + '/landoj', headers=headers, data=data)

def get_landoj_kotizoj():
    url = 'https://uea.org/alighoj/kotiztabelo'
    request = urllib2.Request(url)
    opener = urllib2.build_opener()
    reply = opener.open(request)
    soup = BS(reply.read())
    landoj_kotizoj = soup.findAll('tr')

    for lando in landoj_kotizoj[1:]:
        print "Enmetas nun informojn pri: " + lando.text
        id_lando = insert_lando(lando.contents[0], '')
        insert_kotizo(id_lando, int(lando.contents[1].text) * 100, kategorioj['MG'], '')
        insert_kotizo(id_lando, int(lando.contents[2].text) * 100, kategorioj['MJ'], '')
        insert_kotizo(id_lando, int(lando.contents[3].text) * 100, kategorioj['MA'], '')
        insert_kotizo(id_lando, int(lando.contents[5].text) * 100, kategorioj['KTO'], '')
        insert_kotizo(id_lando, int(lando.contents[6].text) * 100, kategorioj['SZ'], '')
        insert_kotizo(id_lando, int(lando.contents[7].text) * 100, kategorioj['PT'], '')

kategorioj = get_kategorioj()
get_landoj_kotizoj()
