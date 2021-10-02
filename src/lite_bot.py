#!/usr/bin/env python3
import json, os, sys

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.response_selection import get_random_response

botmode = 0

def print_format_table():
    """
    prints table of formatted text format options
    """
    for style in range(8):
        for fg in range(30,38):
            s1 = ''
            for bg in range(40,48):
                format = ';'.join([str(style), str(fg), str(bg)])
                s1 += '\x1b[%sm %s \x1b[0m' % (format, format)
            print(s1)
        print('\n')

def format(style, fg, bg, s):
    f = ';'.join([str(style), str(fg), str(bg)])
    return '\x1b[%sm%s\x1b[0m' % (f, s)

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
              databse="lite_bot"
              )

# Start by training our bot with the ChatterBot corpus data
trainer = ChatterBotCorpusTrainer(chatbot)

#trainer.train('chatterbot.corpus.french')

if(len(sys.argv) == 2):
    convname = sys.argv[1]
    with open(convname) as f:
        conversation = f.readlines()
    #convname = "conversation.txt"
    #convname = "conversation2.txt"
    #convname = "conversation-IAGO.txt"
    chatbot.storage.drop()
    trainer = ListTrainer(chatbot)
    trainer.train(conversation)

# print_format_table()
print("you:")
q = input()
while True:
    if q == "/exit":
        print("\t"+format(3,30,43,"Goobdye"))
        exit()
    if q == "/0": #freemode
        botmode = 0
        print("\t"+format(3,30,43,"Bot Mode Free"))
        print("you:")
    elif q == "/1":
        botmode = 1
        print("\t"+format(3,30,43,"Bot Mode Introduction"))
        print("you:")
    elif q == "/2":
        botmode = 2
        print("\t"+format(3,30,43,"Bot Mode Seduction"))
        print("you:")
    elif q == "/3":
        botmode = 3
        print("\t"+format(3,30,43,"Bot Mode Provocation"))
        print("you:")
    elif q == "/4":
        botmode = 4
        print("\t"+format(3,30,43,"Bot Mode Fuite"))
        print("you:")
    elif q == "/5":
        botmode = 5
        print("\t"+format(3,30,43,"Bot Mode Passe-partout"))
        print("you:")
    else:
        response = chatbot.get_response(q)
        print(format(6,36,40, "bot: "+str(response)))
    q = input()
