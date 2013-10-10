from urllib2 import quote
import subprocess, json
from time import sleep
from os import path

lambes = json.loads(open('../transparencia.json', 'r').read())
estados = ["AC","AL","AM","AP","BA","CE","DF","ES","EX","GO","MA","MG","MS","MT","PA","PB","PE","PI","PR","RJ","RN","RO","RR","RS","SC","SE","SP","TO"]
def generate_image(c):
    if not path.isfile('../static/raw/' + c['file'] + '-hi.png'):
        url = c['url']
        subprocess.call(['phantomjs', 'rasterize.js', url, '.lambe', '../static/raw/' + c['file'] + '-hi.png'])
        sleep(3)
        #subprocess.call(['phantomjs','rasterize.js', url, '.lambe', '../static/raw/' + c['file'] + '.pdf'])
        sleep(8)
    print 'Zzz...'

cache_urls = []
for orgao_a in lambes:
    for orgao_b in lambes:
        for estado_a in lambes[orgao_a]:
            if estado_a in estados and estado_a in lambes[orgao_b]:
                 cache_urls += [{
                    'url' : 'http://127.0.0.1:5000/l/' + quote('/'.join([orgao_a,estado_a,orgao_b,estado_a]).encode('utf-8')),
                    'file' : '-'.join([orgao_a,estado_a,orgao_b,estado_a]).encode('utf-8')
                }]
                 cache_urls += [{
                    'url' : 'http://127.0.0.1:5000/l/' + quote('/'.join([orgao_b,estado_a,orgao_a,estado_a]).encode('utf-8')),
                    'file' : '-'.join([orgao_b,estado_a,orgao_a,estado_a])
                }]

for c in cache_urls:
    generate_image(c)