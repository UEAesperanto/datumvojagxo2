import requests
import urllib
import urllib2
import json
from BeautifulSoup import BeautifulSoup as BS

api_url = "http://localhost:3000"

def get_token():
    data = {'uzantnomo': "skripto", 'pasvorto': "123"}
    response = requests.post(api_url + '/admin/ensaluti', data=data)
    return response.json()['token']

def get_config(valoro):
    url = api_url + "/config/" + valoro
    response = requests.get(url)
    return str(response.json()[valoro])

def insert_kategorioj():
    id_juna = get_config("idJunajGrupoj")

    headers = {'x-access-token': get_token()}

    for data in kategorioj:
        request = requests.post(api_url + '/grupoj', headers=headers, data=data)

        id_grupo = str(request.json()['insertId'])
        data['id'] = id_grupo

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
    return request.json()['insertId']

def insert_kotizo(id_lando, kotizo, id_grupo):
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
        id_lando = insert_lando(lando.contents[0])
        insert_kotizo(id_lando, int(lando.contents[1].text) * 100, kategorioj[0]['id'])
        insert_kotizo(id_lando, int(lando.contents[2].text) * 100, kategorioj[1]['id'])
        insert_kotizo(id_lando, int(lando.contents[3].text) * 100, kategorioj[2]['id'])
        insert_kotizo(id_lando, int(lando.contents[6].text) * 100, kategorioj[3]['id'])
        insert_kotizo(id_lando, int(lando.contents[7].text) * 100, kategorioj[4]['id'])

id_membrecgrupo = get_config("idMembrecgrupo")
id_aldonamembreco = get_config("idAldonaMembrecgrupo")

kategorioj = [
              {
                'mallongigilo': 'MG',
                'nomo': 'Membro kun Gvidlibro',
                'priskribo': 'Individua membro, kiu ricevas nur la Gvidlibron\
                             tra la Esperanto-movado plus la revuon Esperanto rete.',
                'tipo': id_membrecgrupo,
                'juna': False
               },
               {
                 'mallongigilo': 'MJ',
                 'nomo': 'Membro kun Jarlibro',
                 'priskribo': 'Individua membro, kiu ricevas la Jarlibron plus \
                              retan version de la revuo Esperanto.',
                 'tipo': id_membrecgrupo,
                 'juna': False
               },
               {
                 'mallongigilo': 'MA',
                 'nomo': 'Membro Abonanto',
                 'priskribo': 'Individua membro, kiu ricevas la Jarlibron kaj \
                              la revuon Esperanto.',
                 'tipo': id_membrecgrupo,
                 'juna': False
               },
               {
                 'mallongigilo': 'SZ',
                 'nomo': 'Societo Zamenhof',
                 'priskribo': 'Membro de Societo Zamenhof, kiu volas \
                               finance apogi Universalan Esperanto-Asocion. ',
                 'tipo': id_aldonamembreco,
                 'juna': False
               },
               {
                 'mallongigilo': 'PT',
                 'nomo': 'Patrono de TEJO',
                 'priskribo': 'Patrono de TEJO, kiu ricevas la eldonaĵojn de TEJO. ',
                 'tipo': id_aldonamembreco,
                 'juna': True
               }
            ]

insert_kategorioj()
get_landoj_kotizoj()
