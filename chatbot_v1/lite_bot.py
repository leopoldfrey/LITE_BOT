#!/usr/bin/env python3
import json, os, sys

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.response_selection import get_random_response

botmode = 0

# def print_formatColor_table():
#     """
#     prints table of formatColorted text formatColor options
#     """
#     for style in range(8):
#         for fg in range(30,38):
#             s1 = ''
#             for bg in range(40,48):
#                 formatColor = ';'.join([str(style), str(fg), str(bg)])
#                 s1 += '\x1b[%sm %s \x1b[0m' % (formatColor, formatColor)
#             print(s1)
#         print('\n')

def formatColor(style, fg, bg, s):
    f = ';'.join([str(style), str(fg), str(bg)])
    return '\x1b[%sm%s\x1b[0m' % (f, s)

print(formatColor(3,30,43,"Starting Chatbot"))

chatbot = ChatBot('Lite_Bot',
              tie_breaking_method="random_response",
              storage_adapter="chatterbot.storage.SQLStorageAdapter",
              response_selection_method=get_random_response,
              logic_adapters=[
                  "chatterbot.logic.BestMatch"
                  ],
              # input_adapter="chatterbot.input.TerminalAdapter",
              # output_adapter="chatterbot.output.TerminalAdapter",
              filters=["chatterbot.filters.RepetitiveResponseFilter"],
              database="lite_bot",
              read_only=True
              )

print(formatColor(3,30,43,"Chatbot ready"))

if(len(sys.argv) == 2):
    if(sys.argv[1] == "DeleteDB"):
        print("\t"+formatColor(3,30,43,"Deleting Database"))
        chatbot.storage.drop()
        print("\t"+formatColor(3,30,43,"Done, exiting"))
        exit()
    else:
        convname = sys.argv[1]
        with open(convname) as f:
            conversation = f.readlines()
        print("\t"+formatColor(3,30,43,"Training with : "+convname))
        # Start by training our bot with the ChatterBot corpus data
        #convname = "conversation.txt"
        #convname = "conversation2.txt"
        #convname = "conversation-IAGO.txt"
        trainer = ListTrainer(chatbot)
        trainer.train(conversation)
        print("\t"+formatColor(3,30,43,"Done, starting chat"))

# trainer = ChatterBotCorpusTrainer(chatbot)
# trainer.train('chatterbot.corpus.french')

print("you:")
q = input()
while True:
    if q == "/exit":
        print("\t"+formatColor(3,30,43,"Goobdye"))
        exit()
    if q == "/0": #freemode
        botmode = 0
        print("\t"+formatColor(3,30,43,"Bot Mode Free"))
        print("you:")
    elif q == "/1":
        botmode = 1
        print("\t"+formatColor(3,30,43,"Bot Mode Introduction"))
        print("you:")
    elif q == "/2":
        botmode = 2
        print("\t"+formatColor(3,30,43,"Bot Mode Seduction"))
        print("you:")
    elif q == "/3":
        botmode = 3
        print("\t"+formatColor(3,30,43,"Bot Mode Provocation"))
        print("you:")
    elif q == "/4":
        botmode = 4
        print("\t"+formatColor(3,30,43,"Bot Mode Fuite"))
        print("you:")
    elif q == "/5":
        botmode = 5
        print("\t"+formatColor(3,30,43,"Bot Mode Passe-partout"))
        print("you:")
    else:
        response = chatbot.get_response(q)
        print(formatColor(6,36,40, "bot: "+str(response)))
    q = input()
