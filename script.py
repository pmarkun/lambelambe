import csv, codecs
import simplejson as json

arquivo = codecs.open('raw/201307_Transferencias.csv', 'rU')
reader = csv.DictReader((line.replace('\0','') for line in arquivo), delimiter='\t')

def clean(numero):
    if numero:
        return float(numero.replace(',',''))
    else:
        return 0

c = {}
for f in reader:
    if not c.has_key(f['Nome Funcao']):
        c[f['Nome Funcao']] = { f['Sigla Unidade Federa\xe7\xe3o'] : clean(f['Valor Parcela'])}
    else:    
        if not c[f['Nome Funcao']].has_key(f['Sigla Unidade Federa\xe7\xe3o']):
            c[f['Nome Funcao']][f['Sigla Unidade Federa\xe7\xe3o']] = clean(f['Valor Parcela'])
        else:
            c[f['Nome Funcao']][f['Sigla Unidade Federa\xe7\xe3o']] += clean(f['Valor Parcela'])

jason = open('transparencia.json', 'w')
jason.write(json.dumps(c, sort_keys=True, indent=4, separators=(',', ': '), encoding='iso-8859-1'))
jason.close()