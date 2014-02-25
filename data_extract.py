# /usr/bin/python

import sys

'''
Reads the output of mnt.py and tries to make
labeled data for training
'''
def read_data(filename):
    f = open(filename, "r")
    while True:
        line = f.readline()
        if not line:
            break
        line = line.strip()
        sent, tagseq = line.split(' ||| ')
        sentence = sent.split(' ')
        tags = tagseq.split(' ')
        if len(sentence) != len(tags):
            sys.stderr.write(sent+ " "+ tagseq + "\n")
            continue
        i = 0
        for word in sentence:
            tag = tags[i]
#            if tags[i] == "B" or tags[i] == "I":
#                tag = "1"
#            else:
#                tag = "0"
            #print word+"\t"+tag
            i += 1
        print sent + "|||" + tagseq
        #print
    f.close()

def read_vocabulary(trainfile):
    voc = set([])
    f = open(trainfile, "r")
    while True:
        line = f.readline()
        if not line:
            break
        line = line.strip()
        if line == "":
            continue
        word, pos, tag = line.split("\t")
        voc.add(word)
    f.close()
    print len(voc)
    voclist = list(voc)
    i = 0
    vocmap = {}
    for wtype in voclist:
        vocmap[wtype] = i
        i += 1
    return vocmap

if __name__ == "__main__":
    read_data(sys.argv[1])
    #read_vocabulary(sys.argv[1])
