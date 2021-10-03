#!/usr/bin/env python3
import os, json
import urllib3
import certifi
import shutil
from bottle import post, static_file, template, Bottle, request
from upload import Upload
from websocket_server import WebsocketServer
import threading

def new_client(client, server):
    print("Client connected and was given id %d" % client['id'])
    #server.send_message_to_all("Hey all, a new client has joined us")

def client_left(client, server):
    print("Client(%d) disconnected" % client['id'])

def message_received(client, server, message):
    # if len(message) > 200:
    #     message = message[:200]+'..'
    print("Client(%d) said: %s" % (client['id'], message))

def socketSend(message):
	socketServer.send_message_to_all(message)

def initWebSocket():
    PORT=9001
    socketServer = WebsocketServer(PORT)
    socketServer.set_fn_new_client(new_client)
    socketServer.set_fn_client_left(client_left)
    socketServer.set_fn_message_received(message_received)
    threading.Thread(target=socketServer.run_forever).start()
    return socketServer

class FestinTriServer():
    def __init__(self):

        print("Downloading festin.json...")
        http = urllib3.PoolManager(
            cert_reqs="CERT_REQUIRED",
            ca_certs=certifi.where()
        )

        with open("festinTri.json", 'wb') as out:
            r = http.request('GET', "https://grabugemusic.fr/g5/public/data/festin.json", preload_content=False)
            shutil.copyfileobj(r, out)

        print("Loading data...")
        with open("festinTri.json") as f:
            self.data = json.load(f)

        print("Starting WebSocket...")
        self.socketServer = initWebSocket()

        print("FestinTriServer starting...")
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
        with open("festinTri.json", "w") as f:
            json.dump(self.data, f, indent=4)
        thd = Upload("https://grabugemusic.fr/g5/public/data/backupFestin.php", "festinTri.json", self.socketServer)
        thd.start()
        return { "msg": "Sauvegarde en cours"}

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
