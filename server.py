# -*- coding: utf-8 -*-
from flask import Flask, render_template
import json

app = Flask(__name__)
#tmp-load
lambes = json.loads(open('transparencia.json', 'r').read())

@app.route('/')
def index():
    return render_template('lambe.html');

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

    return estados[estado]
@app.template_filter('preposicao')
def preposicao(texto):
    do = ['AC','AP','CE','DF','ES','EX','MA','MS','MT','PA','PI','PR','RJ','RN','RS','TO']
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

    if l['a']['valor'] < l['b']['valor']:
        l['proporcao'] = 'menos'
        l['razao'] = round(l['b']['valor']/l['a']['valor'],1)
    else:
        l['proporcao'] = 'mais'
        l['razao'] = round(l['a']['valor']/l['b']['valor'],1)
    
    if raw:
        return render_template('lambe.html', l=l)
    else:
        return render_template('lambe.html', l=l)

if __name__ == "__main__":
    app.run(debug=True)
