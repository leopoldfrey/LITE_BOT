import json, os, sys

DEBUG = 0

if __name__ == '__main__':
    if(len(sys.argv) == 1):
        print('usage: %s filename %s filename ...')
    else:
        inname = sys.argv[1]
        if os.path.exists(inname):
            outname = os.path.splitext(inname)[0]+"Tri.json";
            outfile = open(outname, 'w')
            print("- Processing "+inname+" > "+outname);
            dict = {}
            with open(inname) as f:
                i = 0
                for line in f:
                    if line == ".\n" :
                        print("LINE WITH POINT")
                    else:
                        dict[i] = {'txt':line, 'in':[]}
                        i = i + 1
                outfile.write(json.dumps(dict, indent = 4))
