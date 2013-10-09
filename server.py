from flask import Flask
import json

app = Flask(__name__)
#tmp-load
lambes = json.loads(open('transparencia.json', 'r').read())

@app.route('/')
def index():
    return 'Hello World!'

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
    
    if raw=='raw':
        return str(l['razao'])
    else:
        return 'Hello'

if __name__ == "__main__":
    app.run(debug=True)
