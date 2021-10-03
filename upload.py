import os
import sys
import requests
from threading import Thread

class upload_in_chunks():

    def __init__(self, socketServer, filename, chunksize=1 << 13):
        self.filename = filename
        self.chunksize = chunksize
        self.totalsize = os.path.getsize(filename)
        self.readsofar = 0
        self.socketServer = socketServer

    def __iter__(self):
        with open(self.filename, 'rb') as file:
            while True:
                data = file.read(self.chunksize)
                if not data:
                    sys.stderr.write("\n")
                    self.socketServer.send_message_to_all('upload=100%')
                    self.socketServer.send_message_to_all('uploadStop')
                    break
                self.readsofar += len(data)
                percent = self.readsofar * 1e2 / self.totalsize
                sys.stderr.write("\r{percent:3.0f}%".format(percent=percent))
                self.socketServer.send_message_to_all('upload=\r{percent:3.0f}%'.format(percent=percent))
                yield data

    def __len__(self):
        return self.totalsize

class Upload(Thread):
    def __init__(self, url, filename, socketServer):
        self.url = url #"https://grabugemusic.fr/g5/public/data/backupFestin.php"
        self.filename = filename #"festinTri.json"
        self.socketServer = socketServer

    def start(self):
        self.socketServer.send_message_to_all('uploadStart')
        requests.post(self.url, data=upload_in_chunks(self.socketServer, self.filename, chunksize=1024))
