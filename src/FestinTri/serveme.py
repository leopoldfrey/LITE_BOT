#!/usr/bin/env python3
import os, json
from bottle import post, static_file, template, Bottle, request

class FestinTriServer():
    def __init__(self):
        print("FestinTriServer starting...")

        with open("../festinTri.json") as f:
            self.data = json.load(f)

        self.host = '0.0.0.0'
        self.port = int(os.environ.get("PORT", 17995))
        self.server = Bottle()
        self.route()
        self.start()

    def start(self):
        # démarrage du serveur
        self.server.run(host=self.host, port=self.port)

    def route(self):
        self.server.route('/', method="GET", callback=self.index)
        self.server.route('/index', method="GET", callback=self.index)
        self.server.route('/index.html', method="GET", callback=self.index)
        self.server.route('/<dir>/<filename>', method="GET", callback=self.serveDir)
        self.server.route('/<filename>', method="GET", callback=self.serve)
        self.server.route('/getSentences/<a>/<b>', method="GET", callback=self.sentences)
        self.server.route('/getMax', method="GET", callback=self.max)
        self.server.route('/save', method="GET", callback=self.save)
        self.server.route('/mod', method="POST", callback=self.mod)

    def index(self):
        return static_file('index.html', root='./')

    def serveDir(self, dir, filename):
        return static_file(filename, root='./'+dir)

    def serve(self, filename):
        return static_file(filename, root='./')

    def sentences(self, a, b):
        #print("getSentences from "+a+" to "+b)
        response = {}
        for i in range(int(a),int(b)):
            response[str(i)] = self.data[str(i)]
        return response

    def save(self):
        with open("../festinTri.json", "w") as f:
            json.dump(self.data, f, indent=4)
        return { "msg": "Sauvegarde effectuée"}

    def max(self):
        print("MAX : "+str(len(self.data)))
        return { 'max': len(self.data) }

    def mod(self):
        for k in request.forms:
            #print(k,type(k))
            j = json.loads(k)
            num = j['num']
            val = j['val']
            self.data[str(num)]['in'] = val
            print(str(num)," ",self.data[str(num)])
        return { "msg": "Modification "+str(num)+" effecuée"}

if __name__ == "__main__":
    server = FestinTriServer()
    server.start()


    {'{"num":3025,"val":[1]}': ''}
