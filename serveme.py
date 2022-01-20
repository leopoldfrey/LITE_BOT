#!/usr/bin/env python3
import os, json, webbrowser
from bottle import post, static_file, template, Bottle, request
from sys import platform as _platform

import threading

class FestinTriServer():
    def __init__(self):

        print("Loading data...")
        self.filename = "festinTri.json"
        self.load()

        #ouverture de google chrome
        # print("___STARTING GOOGLE CHROME___")
        # url = 'http://localhost:17995/'
        # # MacOS
        # if _platform == "darwin":
        #     chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
        # elif _platform == "win32" or _platform == "win64":
        #     chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
        # # Linux
        # # chrome_path = '/usr/bin/google-chrome %s'
        # webbrowser.get(chrome_path).open(url)

        print("FestinTriServer starting...")
        self.host = '0.0.0.0'
        self.port = int(os.environ.get("PORT", 17995))
        self.server = Bottle()
        self.route()
        self.start()

    def load(self):
        print("Loading data "+self.filename)
        with open(self.filename) as f:
            self.data = json.load(f)

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
        self.server.route('/getCat1', method="GET", callback=self.cat1)
        self.server.route('/getCat2', method="GET", callback=self.cat2)
        self.server.route('/getCat3', method="GET", callback=self.cat3)
        self.server.route('/getCat4', method="GET", callback=self.cat4)
        self.server.route('/getCat5', method="GET", callback=self.cat5)
        self.server.route('/getCat0', method="GET", callback=self.cat0)
        self.server.route('/getMax', method="GET", callback=self.max)
        self.server.route('/save', method="GET", callback=self.save)
        self.server.route('/mod', method="POST", callback=self.mod)
        self.server.route('/del', method="POST", callback=self.deleteId)
        self.server.route('/download', method="GET", callback=self.download)
        self.server.route('/upload', method="POST", callback=self.upload)

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
            try:
                response[str(i)] = self.data[str(i)]
            except:
                pass
        return response

    def cat1(self):
        # print("getCat1")
        response = {}
        for i in range(len(self.data)):
            try:
                if 1 in self.data[str(i)]['in'] :
                    response[str(i)] = self.data[str(i)]
            except:
                pass
        return response

    def cat2(self):
        # print("getCat2")
        response = {}
        for i in range(len(self.data)):
            try:
                if 2 in self.data[str(i)]['in'] :
                    response[str(i)] = self.data[str(i)]
            except:
                pass
        return response

    def cat3(self):
        # print("getCat3")
        response = {}
        for i in range(len(self.data)):
            try:
                if 3 in self.data[str(i)]['in'] :
                    response[str(i)] = self.data[str(i)]
            except:
                pass
        return response

    def cat4(self):
        # print("getCat4")
        response = {}
        for i in range(len(self.data)):
            try:
                if 4 in self.data[str(i)]['in'] :
                    response[str(i)] = self.data[str(i)]
            except:
                pass
        return response

    def cat5(self):
        # print("getCat5")
        response = {}
        for i in range(len(self.data)):
            try:
                if 5 in self.data[str(i)]['in'] :
                    response[str(i)] = self.data[str(i)]
            except:
                pass
        return response

    def cat0(self):
        response = {}
        for i in range(len(self.data)):
            try:
                response[str(i)] = self.data[str(i)]
            except:
                pass
        return response

    def save(self):
        with open("festinTri.json", "w") as f:
            json.dump(self.data, f, indent=4)
        # thd = Upload("https://grabugemusic.fr/g5/public/data/backupFestin.php", "festinTri.json", self.socketServer)
        # thd.start()
        return { "msg": "Sauvegarde en cours"}

    def download(self):
        with open("festinTri.json", "w") as f:
            json.dump(self.data, f, indent=4)
        return static_file("festinTri.json", root='./')

    def upload(self):
        upload = request.files.jsonFile
        name, ext = os.path.splitext(upload.filename)
        print("Uploading "+upload.filename)

        if ext not in ('.json'):
            return "File extension not allowed."

        save_path = "."
        file_path = "{path}/{file}".format(path=save_path, file=upload.filename)
        upload.save(file_path, overwrite=True)
        self.filename = file_path
        self.load()
        return "File successfully saved to '{0}'.".format(save_path)

    def max(self):
        # print("MAX : "+list(self.data.keys())[-1])
        return { 'max': list(self.data.keys())[-1] }

    def mod(self):
        for k in request.forms:
            # print("MOD", k)
            j = json.loads(k)
            # print("\t>>", j)
            num = j['num']
            txt = j['txt']
            # txt = txt.replace("_COMMA_", ",").replace("_QUOT1_", "'").replace("_QUOT2_", "\"").replace("_COMMADOT_", ";")
            # print(txt)
            val = j['val']
            if str(num) in self.data:
                self.data[str(num)]['in'] = val
                self.data[str(num)]['txt'] = txt
                print("Modification effectuée >", str(num)," ",self.data[str(num)])
            else:
                self.data[str(num)] = {"txt":txt,"in":val}
                print("Ajout effectué >", str(num)," ",self.data[str(num)])

        return { "msg": "Modification effecuée"}

    def deleteId(self):
        for k in request.forms:
            idx = json.loads(k)['num']
            # print("TODO del", idx)
            self.data.pop(idx)
        return { "msg": "Suppression effectuée"}

if __name__ == "__main__":
    server = FestinTriServer()
    server.start()
