import json, os, sys
from html.parser import HTMLParser

DEBUG = 0

#todo couper au point et supprimer majuscules

if __name__ == '__main__':
    if(len(sys.argv) == 1):
        print('usage: %s filename %s filename ...')
    else:
        outname = "conversation2.txt"
        outfile = open(outname, 'w')
        for x in range(1, len(sys.argv)):
            filename = sys.argv[x]
            if os.path.exists(filename):
                print("- Processing "+filename+" > "+outname);
                with open(filename) as f:
                    for line in f:
                        outfile.write(line)
