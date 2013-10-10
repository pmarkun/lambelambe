from urllib2 import quote
import threading, subprocess, json
from time import sleep
from os import path
from unidecode import unidecode

class RunCmd(threading.Thread):
    def __init__(self, cmd, timeout):
        threading.Thread.__init__(self)
        self.cmd = cmd
        self.timeout = timeout

    def run(self):
        self.p = subprocess.Popen(self.cmd, close_fds=True)
        self.p.wait()

    def Run(self):
        self.start()
        self.join(self.timeout)

        if self.is_alive():
            self.p.terminate()
            self.join()

lambes = json.loads(open('../transparencia.json', 'r').read())
estados = ["AC","AL","AM","AP","BA","CE","DF","ES","EX","GO","MA","MG","MS","MT","PA","PB","PE","PI","PR","RJ","RN","RO","RR","RS","SC","SE","SP","TO"]
def generate_image(c):
    if not path.isfile('../static/raw/' + c['file'] + '-hi.png'):
        url = c['url']
        RunCmd(['phantomjs', 'rasterize.js', url, '.lambe', '../static/raw/' + c['file'] + '-hi.png'], 10).run()
    print 'Zzz...'

cache_urls = []
for orgao_a in lambes:
    for orgao_b in lambes:
        for estado_a in lambes[orgao_a]:
            if estado_a in estados and estado_a in lambes[orgao_b]:
                 cache_urls += [{
                    'url' : 'http://127.0.0.1:5000/l/' + quote('/'.join([orgao_a,estado_a,orgao_b,estado_a]).encode('utf-8')),
                    'file' : unidecode('-'.join([orgao_a,estado_a,orgao_b,estado_a]))
                }]
                 cache_urls += [{
                    'url' : 'http://127.0.0.1:5000/l/' + quote('/'.join([orgao_b,estado_a,orgao_a,estado_a]).encode('utf-8')),
                    'file' : unidecode('-'.join([orgao_b,estado_a,orgao_a,estado_a]))
                }]

for c in cache_urls:
    generate_image(c)