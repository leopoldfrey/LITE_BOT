from websocket_server import WebsocketServer
import threading

def new_client(client, server):
    print("New client connected and was given id %d" % client['id'])
    server.send_message_to_all("Hey all, a new client has joined us")

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
    socketServer = WebsocketServer(self.PORT)
    socketServer.set_fn_new_client(new_client)
    socketServer.set_fn_client_left(client_left)
    socketServer.set_fn_message_received(message_received)
    threading.Thread(target=server.run_forever).start()
    return socketServer
