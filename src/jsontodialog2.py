import json, os, sys
from html.parser import HTMLParser

DEBUG = 0

class VersParser():
    def __init__(self, filename, outname):
        with open(filename) as file:
            data = json.load(file)

        outfile = open(outname, 'w')

        if(DEBUG):
            print("\t"+data['pieces'][0]['title'])
        for act in data['pieces'][0]['actes']:
            a = data['pieces'][0]['actes'][act]
            if(DEBUG):
                print("\t\t"+act+" "+a['title'])
            for scene in a['scenes']:
                s = a['scenes'][scene];
                if(DEBUG):
                    print("\t\t\t"+scene+" "+s['title'])
                for rep in s['repliques']:
                    r = s['repliques'][rep];
                    if(DEBUG):
                        print("\t\t\t\t"+rep+" "+r['personnage'])
                    for vers in r['vers']:
                        v = r['vers'][vers]
                        v = v.replace("              ", "")
                        v = v.replace('\n','')
                        if(DEBUG):
                            print("\t\t\t\t\t"+vers+" "+v)
                        outfile.write(v+" ")
                    outfile.write('\n')

def parseFile(filename):
    if os.path.exists(filename):
        outname = os.path.splitext(filename)[0]+".txt";
        print("- Parsing "+filename+" > "+outname);
        VersParser(filename, outname)

if __name__ == '__main__':
    if(len(sys.argv) == 1):
        print('usage: %s filename %s filename ...')
    else:
        for x in range(1, len(sys.argv)):
            parseFile(sys.argv[x])
