import json, os, sys

DEBUG = 0

if __name__ == '__main__':
    if(len(sys.argv) == 1):
        print('usage: %s filename %s filename ...')
    else:
        outname = "festin.txt"
        outfile = open(outname, 'w')
        for x in range(1, len(sys.argv)):
            filename = sys.argv[x]
            if os.path.exists(filename):
                print("- Processing "+filename+" > "+outname);
                with open(filename) as f:
                    for line in f:
                        outfile.write(line)