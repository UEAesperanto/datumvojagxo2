import requests
import urllib
import urllib2
import re
import cookielib
import json
import configparser

config = configparser.ConfigParser()
config.read('config.cfg')

def get_token(token):
    if (token is None) or (token == ''):
        data = {'uzantnomo': config['api']['uzantnomo'], 'pasvorto': config['api']['pasvorto']}
        response = requests.post(config['api']['url'] + '/admin/ensaluti', data=data)
        return response.json()['token']
    else:
        return token

def ensaluti(opener):
    url = 'https://db.uea.org/index.php'
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'

    data_login = urllib.urlencode(
                 {"uvorto": config['nuna_db']['uzantnomo'],
                 "pvorto": config['nuna_db']['pasvorto']})
    login_request = urllib2.Request(url, data_login)
    opener.open(login_request)
