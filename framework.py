# /usr/bin/python
from features import extract

from time import time
import sys, re

def write_weights(weights, iteration):
    filename = "wfinal/"+ str(time()%10000)+"_" + str(iteration) + ".dat"
    f = open(filename, "w")
    for k,v in weights.iteritems():
        f.write(str(k)+" "+str(v)+"\n")
    f.close()
    sys.stderr.write("weights in " + filename +"\n")

def read_features(featsfile):
    featlist = []
    feats = open(featsfile, 'r')
    while True:
        line = feats.readline()
        if not line:
            break
        featlist.append(int(line.strip()))
    feats.close()
    return featlist
    
def extract_all_train_features(sents, tagseqs, postagseqs, info):
    featset = set([])
    i = 0
    for sent in sents:
        sys.stderr.write(str(i) + "\r")
        j = 0
        for word in sent:
            tag = tagseqs[i][j]
            postag = postagseqs[i][j]
            if j == 0: # first position
               prev = '*'
            else:
               prev = tagseqs[i][j-1]
            featset.update(extract(word, tag, prev, postag, info)) # get a list of all features possible
            j += 1
        # features for the last label
        featset.update(extract('', '<STOP>', tag, '', info))
        i += 1
    featlist = list(featset)
    for f in featlist:
        print f
    return featlist

def read_data(datafile):
    data = open(datafile, 'r')
    sents = []
    tagseqs = []
    postagseqs = []
    sent = []
    tags = []
    postags = []
    while 1:
        line = data.readline()
        if not line:
	   break
        line = line.strip()
	if line == "":
	    sents.append(sent)
	    tagseqs.append(tags)
	    postagseqs.append(postags)
	    sent = []
	    tags = []
	    postags = []
	    continue
        
	word, pos, tag = line.split("\t")
	sent.append(word.strip())
	tags.append(tag.strip())
	postags.append(pos.strip())
    data.close()
    return sents, tagseqs, postagseqs

def get_maps(sents, postagseqs, gazfile):
    vocset = set([])
    pset = set([])

    for sent in sents:
        vocset.update(sent)
    for postags in postagseqs:
        pset.update(postags)

    voclist = list(vocset)
    plist = list(pset)

    i = 1
    vocmap = {}
    for wtype in voclist:
        vocmap[wtype] = i
        i += 1

    j = 1
    pmap = {}
    for ptype in plist:
        pmap[ptype] = j
        j += 1

    lmap = {'B':1, 'I':2, 'O':3}
    return (vocmap, pmap, lmap, get_gazetteer(gazfile)) 

def get_gazetteer(gazfile):
    if gazfile == "x.dat":
        return None
    gmap = {}
    g = open(gazfile, 'r')
    j = 1
    while True:
       line = g.readline()
       if not line:
           break
       word, score = line.strip().split(" ")
       gmap[word] = int(float(score))
       j += 1
    g.close()
    return gmap

def get_all(trainfile, gazfile, featfile):
    sys.stderr.write("reading training data\n")
    sents, tagseqs, postagseqs = read_data(trainfile)
    info = get_maps(sents, postagseqs, gazfile)
 
    sys.stderr.write("extracting features from " + str(len(sents)) + " sentences\n")
    #featlist = extract_all_train_features(sents,tagseqs, postagseqs, info)
    featlist = read_features(featfile)

    return sents, tagseqs, postagseqs, featlist, info

if __name__ == "__main__":
    sentset, labelset, postagset, all_feats, info = get_all(sys.argv[1], sys.argv[2], sys.argv[3])
