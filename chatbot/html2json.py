import json, os, sys
from html.parser import HTMLParser

DEBUG = 0

class TheatreParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.curTag = ""
        self.curId = ""
        self.curClass = ""
        self.waitTitlePiece = False
        self.foundTitlePiece = False
        self.waitTitleAct = False
        self.foundTitleAct = False
        self.waitTitleScene = False
        self.foundTitleScene = False
        self.waitSpeaker = False
        self.foundSpeaker = False
        self.foundVers = False
        self.data = ""
        self.act = ""
        self.scene = ""
        self.replique = ""
        self.vers = -1
        self.out = {}

    def handle_starttag(self, tag, attrs):
        self.curTag = tag
        data = {key:value for (key,value) in attrs}
        self.curId = data.get('id')
        self.curClass = data.get('class')

        if(self.curTag == 'section'):
            if(self.curId == 'body'):
                # print("START PIECE")
                self.data = ""
                self.waitTitlePiece = True
            elif ("act" in self.curClass or "prelude" in self.curClass):
                # print("START ACT")
                self.waitTitleAct = True
                self.act = self.curId
            elif ('scene' in self.curClass):
                # print("START SCENE")
                self.waitTitleScene = True
                self.scene = self.curId
        elif(self.curTag == 'h1'):
            if(self.waitTitlePiece):
                #print("PIECE TITLE")
                self.foundTitlePiece = True
                self.data = ""
                self.waitTitlePiece = False
        elif(self.curTag == 'h2'):
            if(self.waitTitleAct):
                #print("ACT TITLE")
                self.foundTitleAct = True
                self.data = ""
                self.waitTitleAct = False
        elif(self.curTag == 'h3'):
            if(self.waitTitleScene):
                #print("SCENE TITLE")
                self.foundTitleScene = True
                self.data = ""
                self.waitTitleScene = False
        elif(self.curTag == 'div'):
            if(self.curClass == 'titlePart main' or self.curClass == 'titlePart main uc'):
                self.foundTitlePiece = True
                self.data = ""
            elif(self.curClass == 'titleStmt'):
                self.waitTitlePiece = True
            elif(self.curClass == "sp"):
                if(self.scene == ""):
                    return;
                #print("REPLIQUE")
                self.replique = self.curId
                self.vers = -1
                self.waitSpeaker = True
                self.speaker = ""
            elif(self.curClass == "l" or self.curClass == "l part-I" or self.curClass == "l part-F" or self.curClass == "l part-M" or self.curClass == "l first"):# or "l part" in self.curClass):
                if(self.scene == ""):
                    return
                if(self.replique == ""):
                    return
                self.vers += 1
                self.foundVers = True
                self.data = ""

        elif(self.curTag == 'p'):
            if(self.waitSpeaker):
                #print("ROLE")
                self.foundSpeaker = True
                self.speaker = ""
                self.waitSpeaker = False
            elif("p autofirst" in self.curClass):
                if(self.scene == ""):
                    return
                if(self.replique == ""):
                    return
                #print("AUTOFIRST s:"+self.scene)
                #print("AUTOFIRST r:"+self.replique)
                #print("AUTOFIRST v:"+str(self.vers))
                self.vers += 1
                self.foundVers = True
                self.data = ""

    def handle_endtag(self, tag):
        if(tag == 'a'):
            return
        if(tag == "section"):
            #self.act = ""
            self.scene = ""
            self.replique = ""
            self.vers = -1
            #print("End Section")
        if(self.foundVers and (tag == 'div' or tag == 'p')):
            self.foundVers = False
            if(DEBUG):
                print("\t\t\t\t"+self.data)
            if(self.speaker == ""):
                self.out['pieces'][0]['actes'][self.act]['scenes'][self.scene]['repliques'][self.replique] = {'vers': {}}
            #if(DEBUG):
            #    print(self.act+" "+self.scene+" "+self.replique+" Vers "+str(self.vers)+" ("+self.speaker+")")#+self.data)
            self.out['pieces'][0]['actes'][self.act]['scenes'][self.scene]['repliques'][self.replique]['vers'][self.vers] = self.data
        elif(self.foundTitlePiece):
            self.foundTitlePiece = False
            if(DEBUG):
                print("Titre : "+self.data)
            self.out['pieces'] = [1]
            self.out['pieces'][0] = {'title': self.data}
            self.out['pieces'][0]['actes'] = {}
        elif(self.foundTitleAct):
            self.foundTitleAct = False
            if(DEBUG):
                print("\tActe "+self.act+" : "+self.data)
            self.out['pieces'][0]['actes'][self.act] = { 'title': self.data, 'scenes': {}}
        elif(self.foundTitleScene):
            self.foundTitleScene = False
            if(self.act == ""):
                # print("NO ACT")
                self.act = "-"
                self.out['pieces'][0]['actes'][self.act] = { 'title': "", 'scenes': {}}
            if(self.waitTitleAct):
                # print("NO TITLE")
                self.waitTitleAct = False
                self.out['pieces'][0]['actes'][self.act] = { 'title': "", 'scenes': {}}

            #print(self.act+" "+self.scene+" "+json.dumps(self.out['pieces'][0]['actes']))#+" "+self.replique+" Vers "+str(self.vers)+" ("+self.speaker+")")#+self.data)
            self.out['pieces'][0]['actes'][self.act]['scenes'][self.scene] = { 'title': self.data, 'repliques': {} }
            if(DEBUG):
                print("\t\tScène "+self.scene+" : "+self.data)
            self.replique = ""

    def handle_data(self, data):
        if(self.curTag == "a"):# or self.curTag == "small"):
            return
        if(self.foundVers):
            if(self.curTag == 'small' or self.curTag == 'span'):
                self.curTag = 'div'
            else:
                self.data += data
        elif(self.foundSpeaker):
            self.speaker = data.replace(',', '').replace('.', '')
            self.foundSpeaker = False
            if(DEBUG):
                print("\t\t\tRéplique "+self.replique+" : "+self.speaker)
            self.out['pieces'][0]['actes'][self.act]['scenes'][self.scene]['repliques'][self.replique] = {'personnage':self.speaker, 'vers': {}}
        elif(self.foundTitlePiece or self.foundTitleAct or self.foundTitleScene):
            self.data += data

def parseFile(filename):
    if os.path.exists(filename):
        outname = os.path.splitext(filename)[0]+".json";
        print("- Parsing "+filename+" > "+outname);
        with open(filename) as file:
            contents = file.read()
        parser = TheatreParser()
        parser.feed(contents)
        with open(outname, 'w') as outfile:
            json.dump(parser.out, outfile, indent=4)

if __name__ == '__main__':
    if(len(sys.argv) == 1):
        print('usage: %s filename %s filename ...')
    else:
        for x in range(1, len(sys.argv)):
            parseFile(sys.argv[x])
