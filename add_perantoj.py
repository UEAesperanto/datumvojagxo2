#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# Dependas de "add_landoj_kotizoj.py"
import requests
import urllib
import urllib2
import json
import configparser
from BeautifulSoup import BeautifulSoup as BS

api_url = config['api']['url'],
token = ''

def get_token():
    if(token == ''):
        data = {'uzantnomo': config['api']['uzantnomo'], 'pasvorto': config['api']['pasvorto']}
        response = requests.post(api_url + '/admin/ensaluti', data=data)
        return response.json()['token']
    else:
        return token

def get_landoj():
    response = requests.get(api_url + '/landoj')
    return dict(map(lambda x: [x['landkodo'], x['id']], response.json()))

def post_perantoj(data):
    print "Enmetante datumojn de peranto: " + data['publikaNomo']
    headers = {'x-access-token': get_token()}
    request = requests.post(api_url + '/perantoj', headers=headers, data=data)
    if request.status_code != 201:
        print request.status_code, data
    else:
        print "Sukcese enmetita"

def get_perantoj():
    url = 'https://uea.org/alighoj/perantoj'
    request = urllib2.Request(url)
    opener = urllib2.build_opener()
    reply = opener.open(request)
    soup = BS(reply.read())
    perantoj = soup.findAll('tr')
    landoj = get_landoj()

    for i in range(0, len(perantoj)):
        if (perantoj[i].img):
            landkodo = perantoj[i].img['src'].split('/')[3].split('.')[0]
        else:
            landkodo = perantoj[i - 1].img['src'].split('/')[3].split('.')[0]
        try:
            idLando = landoj[landkodo]
            peranto_info = perantoj[i].findAll('a', {'class': 'retadreso'})[0]
            publikaNomo = peranto_info['title'].split(':')[1][1:]
            retadreso = peranto_info['j'] + '@' + peranto_info['rel']
            data = {'idLando': idLando, 'publikaNomo': publikaNomo, 'retadreso': retadreso}
            post_perantoj(data)
        except Exception as e:
            print(e)
            pass

get_perantoj()
