#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# Dependas de "add_landoj_kotizoj.py"
import requests
import json
import configparser
import util
from BeautifulSoup import BeautifulSoup as BS

config = configparser.ConfigParser()
config.read('config.cfg')

api_url = config['api']['url']

def get_uzantoj(token):
    headers = {'x-access-token':  util.get_token(token)}
    request = requests.get(api_url + '/uzantoj', headers=headers)
    if request.status_code == 200:
        return request.json()
    elif (request.status_code == 400) or (request.status_code == 403):
        token = ''
        token = util.get_token(token)
        get_uzantoj(token)

def get_retlisto_id():
    request = requests.get(api_url + '/dissendoj/retlistoj')
    return request.json()[0]['id']

def aldoni_uzantoj_retlisto(uzantoj, id_retlisto):
    for uzanto in uzantoj:
        if uzanto['retposxto']:
            data = {'retadreso': uzanto['retposxto']}
            url = api_url + '/dissendoj/retlistoj/' + str(id_retlisto) + '/abonantoj'
            request = requests.post(url, data)

token = ''
token = util.get_token(token)
uzantoj = get_uzantoj(token)
id_retlisto = get_retlisto_id()
aldoni_uzantoj_retlisto(uzantoj, id_retlisto)
