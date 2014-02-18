# /usr/bin/python

from __future__ import division
import viterbi
from features import read_data, get_maps
import sys

def read_weights(weightsfile):
    weights = {}
    feats = open(weightsfile, 'r')
    while 1:
        line = feats.readline()
        if not line:
            break
        line = line.strip()
        f, wt = line.split(' ')
        weights[int(f)] = float(wt)
    feats.close()
    return weights

def decode(sents, goldtagseqs, postagseqs, info, weights) : #estfile, weightsfile):
    labelset = ['B', 'I', 'O', '*']

    tp = 0
    acc = 0.0
    tot = 0
    tot_rec = 0
    tot_prec = 0
    
    sys.stderr.write("total test sentences = " + str(len(sents)) + "\n\n")
    for i in range(len(sents)):
        sys.stderr.write(str(i) + "\r")
	sent = sents[i]
        postags = postagseqs[i]

	tags, f = viterbi.execute(sent, labelset, postags, weights, info)
        for j in range(len(tags)):
            print sent[j]+"\t"+postags[j]+"\t"+tags[j]
            if tags[j] == goldtagseqs[i][j]:
                acc += 1
                if goldtagseqs[i][j] in ['B','I']:
                    tp += 1
            if goldtagseqs[i][j] in ('B', 'I'):
                tot_rec += 1
            if tags[j] in ('B', 'I'):
                tot_prec += 1
        print
        
        tot += len(tags)
        #print ' '.join(sent)
	#print ' '.join(tags), '\n', ' '.join(tagseqs[i])
        #print
    sys.stderr.write("accuracy  = " + str(acc/tot) + "\n")
    sys.stderr.write("recall    = " + str(tp/tot_rec) + "\n")
    sys.stderr.write("precision = " + str(tp/tot_prec) + "\n\n")

if __name__ == "__main__":
    testfile = sys.argv[1]
    weightsfile = sys.argv[2]
    gazfile = sys.argv[3]
    sents, goldtagseqs, postagseqs = read_data(testfile)
    info = get_maps(sents, postagseqs, gazfile)
    weights = read_weights(weightsfile)
    decode(sents, goldtagseqs, postagseqs, info, weights)

