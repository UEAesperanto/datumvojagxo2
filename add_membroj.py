# coding=<uft-8>
import urllib
import urllib2
import re
import cookielib
import json
from BeautifulSoup import BeautifulSoup as BS

jar = cookielib.FileCookieJar("cookie")
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))

def ensaluti():
    url = 'https://db.uea.org/index.php'
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'

    data_login = urllib.urlencode(
                 {"uvorto":"xyz",
                 "pvorto":"xyz"})
    login_request = urllib2.Request(url, data_login)
    opener.open(login_request)

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
    persona_nomo = ''.join(personaj_nomoj)

    # prenas familianomo
    familia_nomo = uzanto[1].contents[1].text

    # prenas adreso
    adreso = uzanto[2].text.replace('&nbsp;', '')

    #prenas urbo
    urbo = uzanto[3].text.replace('&nbsp;', '')

    #prenas posxtkodo
    posxtkodo = uzanto[4].text.replace('&nbsp;', '')

    #prenas landkodo
    landkodo = uzanto[5].img['alt']

    #prenas retadreso
    retadreso = uzanto[6].text.replace('&nbsp;', '')

    #prenas naskigxtago
    naskigxtago = uzanto[7].text.replace('&nbsp;', '').replace('/','-')

    #prenas membrecoj
    membrecoj = uzanto[8].text.replace('&nbsp;', '').replace(' ', '').split(',')

    uzanto_json = {'ueakodo': ueakodo,
                   'titolo': titolo,
                   'personanomo': persona_nomo,
                   'familianomo': familia_nomo,
                   'adreso': adreso,
                   'urbo': urbo,
                   'posxtkodo': posxtkodo,
                   'landkodo': landkodo,
                   'retadreso': retadreso,
                   'naskigxtago': naskigxtago,
                   'membrecoj': membrecoj}
    homo_json = open("homo1.json", "w")
    #homo_json.write(json.dumps(uzanto_json))

#html_file = open("browser.html", "r")
#homo_1 = open("homo1.html", "w")
reply_data_listo = html_file.read()
# reply_data_listo = get_membroj()
soup = BS(reply_data_listo)
uzantoj = soup.findAll('tr')
uzantoj = uzantoj[2:len(uzantoj)]

soup = BS(str(uzantoj[0]))
uzanto = soup.findAll('td')
krei_uzanton(uzanto)
# print len(uzanto)
# for i in uzanto:
#     print i.contents

#html_file.write(reply_data_listo)
#html_file.close()
#homo_1.write(str(uzantoj[0]))
#homo_1.close()
