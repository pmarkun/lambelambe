# -*- coding: utf-8 -*-
from flask import Flask, render_template
import json, math, os, subprocess
import threading, subprocess
from urllib2 import quote, unquote

here = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
#tmp-load
lambes = json.loads(open(here+'/static/transparencia.json', 'r').read())


class RunCmd(threading.Thread):
    def __init__(self, cmd, timeout):
        threading.Thread.__init__(self)
        self.cmd = cmd
        self.timeout = timeout

    def run(self):
        self.p = subprocess.Popen(self.cmd)
        self.p.wait()

    def Run(self):
        self.start()
        self.join(self.timeout)

        if self.is_alive():
            self.p.terminate()
            self.join()



def generate_image(l, timeout):
    if l['a']['valor'] <= l['b']['valor']:
        image_path = '-'.join([l['b']['orgao'],l['b']['estado'],l['a']['orgao'],l['a']['estado']])
        image_url = '/'.join([l['b']['orgao'],l['b']['estado'],l['a']['orgao'],l['a']['estado']])
    else:
        image_path = '-'.join([l['a']['orgao'],l['a']['estado'],l['b']['orgao'],l['b']['estado']])
        image_url = '/'.join([l['b']['orgao'],l['b']['estado'],l['a']['orgao'],l['a']['estado']])

    image_url = quote(image_url.encode('utf-8'))
    url = ('http://127.0.0.1:5000'  + '/l/' + image_url + '').encode('utf-8')
    RunCmd(['phantomjs', here+'/scripts/rasterize.js', url, '.lambe', here+'/static/raw/' + image_path + '-hi.png'], timeout).Run()
    RunCmd(['phantomjs', here+'/scripts/rasterize.js', url, '.lambe', here+'/static/raw/' + image_path + '-a3.pdf'], timeout).Run()
    return image_path + '-hi.png'

@app.route('/')
def index():
    return render_template('lambe.html');

@app.template_filter('square')
def square(n):
    return int(math.sqrt(n))

@app.template_filter('longo')
def longo(estado):
    estados = {
        "AC": "Acre",
        "AL": "Alagoas",
        "AM": "Amazonas",
        "AP": "Amapa",
        "BA": "Bahia",
        "CE": "Ceara",
        "DF": "Distrito Federal",
        "ES": "Espírito Santo",
        "EX": "EX",
        "GO": "Goias",
        "MA": "Maranhão",
        "MG": "Minas Gerais",
        "MS": "Mato Grosso do Sul",
        "MT": "Mato Grosso",
        "PA": "Pará",
        "PB": "Paraiba",
        "PE": "Pernambuco",
        "PI": "Piaui",
        "PR": "Paraná",
        "RJ": "Rio de Janeiro",
        "RN": "Rio Grande do Norte",
        "RO": "Rondônia",
        "RR": "Roraima",
        "RS": "Rio Grande do Sul",
        "SC": "Santa Catarina",
        "SE": "Sergipe",
        "SP": "São Paulo",
        "TO": "Tocantins"
    }
    return estados[estado].decode('utf-8')
@app.template_filter('preposicao')
def preposicao(texto):
    do = ['AM','AC','AP','CE','DF','ES','EX','MA','MS','MT','PA','PI','PR','RJ','RN','RS','TO']
    de = ['AL','GO','MG','PE','RO','RR','SC','SP']
    da = ['BA','PB']

    if texto in do:
        return 'no'
    if texto in da:
        return 'na'
    if texto in de:
        return 'em'

@app.template_filter('medida')
def medida(valor):
    if valor > 1000:
        x = round(valor/1000,1)
        x = str(x) + u' mil'
    if valor > 1000000:
        x = round(valor/1000000,1)
        if x < 2:
            x = str(x) + u' milhão'
        else:    
            x = str(x) + u' milhões'
    if valor > 1000000000:
        x = round(valor/1000000000,1)
        if x < 2:
            x = str(x) + u' bilhão'
        else:
            x = str(x) + u' bilhões'
    return x

@app.route('/l/<orgao_a>/<estado_a>/<orgao_b>/<estado_b>')
@app.route('/l/<orgao_a>/<estado_a>/<orgao_b>/<estado_b>/<raw>')
def lambe(orgao_a,estado_a,orgao_b,estado_b,raw=False):
    orgao_a = unquote(orgao_a)
    estado_a = unquote(estado_a)
    orgao_b = unquote(orgao_b)
    estado_b = unquote(estado_b)
    
    l = {
        'a' : {
            "estado" : estado_a,
            "orgao" : orgao_a,
            "valor" : lambes[orgao_a][estado_a]
        },
        'b' : {
            "estado" : estado_b,
            "orgao" : orgao_b,
            "valor" : lambes[orgao_b][estado_b]
        }
    }

    if l['a']['valor'] <= l['b']['valor']:
        l['proporcao'] = 'menos'
        #hackish?
        l['razao'] = round((l['b']['valor']-l['a']['valor'])/l['a']['valor'],1)
        l['razao_g'] = round(l['b']['valor']/l['a']['valor'],1)
        image_path = '-'.join([l['a']['orgao'],l['a']['estado'],l['b']['orgao'],l['b']['estado']])
    else:
        l['proporcao'] = 'mais'
        l['razao'] = round(l['a']['valor']/l['b']['valor'],1)
        image_path = '-'.join([l['a']['orgao'],l['a']['estado'],l['b']['orgao'],l['b']['estado']])
    
    if os.path.isfile(here+'/static/raw/' + image_path+'-hi.png'):
        l['image'] = image_path
    else:
        #pass
        t = threading.Thread(target=generate_image, args=(l, 3))
        t.start()
        #generate_image(l, 10)
    return render_template('lambe.html', l=l)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
