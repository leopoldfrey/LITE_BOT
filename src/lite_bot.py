import json, os, sys

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

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

chatbot = ChatBot('Lite_Bot')

# Start by training our bot with the ChatterBot corpus data
trainer = ChatterBotCorpusTrainer(chatbot)

#trainer.train('chatterbot.corpus.french')

#convname = "conversation.txt"
convname = "conversation2.txt"
#convname = "conversation-IAGO.txt"

with open(convname) as f:
    conversation = f.readlines()

trainer = ListTrainer(chatbot)
trainer.train(conversation)

#response = chatbot.get_response('Tu peux sauver le monde ?')
# input = ' '.join(sys.argv[1:])
# print(format(6,36,40, "you: "+input))
# response = chatbot.get_response(input)
# print(format(6,32,40, "bot: "+str(response)))

print("you:")
q = input()
while True:
    # print("you: "+q)
    response = chatbot.get_response(q)
    print(format(6,36,40, "bot: "+str(response)))
    q = input()
