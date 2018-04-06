#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import configparser
import requests
import util

config = configparser.ConfigParser()
config.read('config.cfg')

api_url = config['api']['url']

def get_config(valoro):
    url = api_url + "/config/" + valoro
    response = requests.get(url)
    return str(response.json()[valoro])

id_membrecgrupo = get_config("idMembrecgrupo")
id_aldonamembreco = get_config("idAldonaMembrecgrupo")
id_laborgrupo = get_config("idLaborgrupo")

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
               },
               {
                'mallongigilo': 'KTO',
                'nomo': 'Abono al la revuo Kontakto',
                'priskribo': 'Se vi estas en TEJO aĝo (ĝis 35 jarojn), aliĝante kiel Membro Abonanto\
                              aŭ Membro kun Jarlibro, vi JAM ricevos abonon de revuo Kontakto',
                'tipo': id_aldonamembreco,
                'juna': True
               },
               {
                'mallongigilo': 'ES',
                'nomo': 'Estraro',
                'priskribo': 'La Estraro efektivigas la ĝeneralan agadon de UEA.',
                'tipo': id_laborgrupo,
                'juna': False
               },
               {
                'mallongigilo': 'KOM.A',
                'nomo': 'Komitatano A',
                'priskribo': 'La Komitato estas la gvid-organo de UEA. \
                             Komitatanoj: A estas elektitaj de aliĝintaj asocioj',
                'tipo': id_laborgrupo,
                'juna': False
               },
               {
                 'mallongigilo': 'KOM.B',
                 'nomo': 'Komitatano B',
                 'priskribo': 'La Komitato estas la gvid-organo de UEA. \
                                Komitatanoj: B elektitaj de Individuaj Membroj',
                  'tipo': id_laborgrupo,
                  'juna': False
                },
               {
                 'mallongigilo': 'KOM.C',
                 'nomo': 'Komitatano C',
                 'priskribo': 'La Komitato estas la gvid-organo de UEA. \
                               Komitatanoj: C alelektitaj de komitatanoj A kaj B.',
                  'tipo': id_laborgrupo,
                  'juna': False
                },
                {
                 'mallongigilo': 'd',
                 'nomo': 'Delegito',
                 'priskribo': 'Delegitoj estas voluntulaj reprezentantoj \
                               de UEA tra la mondo. La delegito \
                               okupiĝas pri la loka movado ĝenerale
                  'tipo': id_laborgrupo,
                  'juna': False
                },
                {
                  'mallongigilo': 'fd',
                  'nomo': 'Faka delegito',
                  'priskribo': 'Delegitoj estas voluntulaj reprezentantoj \
                                de UEA tra la mondo. \
                                Fakdelegito okupiĝas pri temo, pri kiu li aŭ ŝi\
                                havas aparte grandan scion, sperton aŭ intereson..',
                   'tipo': id_laborgrupo,
                   'juna': False
               },
               {
                 'mallongigilo': 'jd',
                 'nomo': 'Junulara delegito',
                 'priskribo': 'Delegitoj estas voluntulaj reprezentantoj \
                               de UEA tra la mondo. \
                               Junualaraj delegitoj okupiĝas pri la loka junulara movado.',
                  'tipo': id_laborgrupo,
                  'juna': True
              },
             {
               'mallongigilo': 'vd',
               'nomo': 'Vicdelegito',
               'priskribo': 'Delegitoj estas voluntulaj reprezentantoj \
                             de UEA tra la mondo. \
                             Vicdelegitoj helpas kaj anstataŭas la Delegiton, speciale en grandaj urboj',
                'tipo': id_laborgrupo,
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

def insert_kategorioj(token):
    token = util.get_token(token)
    id_juna = get_config("idJunajGrupoj")
    headers = {'x-access-token': token}

    for data in kategorioj:
        request = requests.post(api_url + '/grupoj', headers=headers, data=data)

        if (request.status_code == 400) or (request.status_code == 403):
            token = ''
            token = util.get_token(token)
            headers = {'x-access-token': token}
            request = requests.post(api_url + '/grupoj', headers=headers, data=data)

        if request.status_code == 500:
            print data

        if('insertId' in request.json()):
            id_grupo = str(request.json()['insertId'])
            print id_grupo
            if(data['tipo']):
                url = api_url + '/grupoj/kategorioj/' + data['tipo'] + '/sub/' + id_grupo
                requests.post(url, headers=headers)

            if(data['juna']):
                url = api_url + '/grupoj/kategorioj/' + id_juna + '/sub/' + id_grupo
                requests.post(url, headers=headers)


insert_kategorioj('')
