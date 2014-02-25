# /usr/bin/python

from __future__ import division
import viterbi
from framework import read_data, get_maps
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

    tp_bi = 0
    tp_o = 0
    acc = 0.0
    tot = 0
    tot_rec_bi = 0
    tot_rec_o = 0
    tot_prec_bi = 0
    tot_prec_o = 0
    
    sys.stderr.write("total test sentences = " + str(len(sents)) + "\n")
    for i in range(len(sents)):
        sys.stderr.write(str(i) + "\r")
	sent = sents[i]
        postags = postagseqs[i]

	tags = viterbi.execute(sent, labelset, postags, weights, info)
        for j in range(len(tags)):
            if tags[j] == goldtagseqs[i][j]:
                acc += 1
            if goldtagseqs[i][j] in ('B','I') and tags[j] in ('B','I'):
                tp_bi += 1
            elif goldtagseqs[i][j] == "O" and tags[j] == "O":
                tp_o += 1

            if goldtagseqs[i][j] in ('B', 'I'):
                tot_rec_bi += 1
            else:
                tot_rec_o += 1
            if tags[j] in ('B', 'I'):
                tot_prec_bi += 1
            else:
                tot_prec_o += 1
            print sent[j]+"\t"+postags[j]+"\t"+goldtagseqs[i][j]+"\t"+tags[j]
        print
        
        tot += len(tags)
    sys.stderr.write("accuracy     = "    + str(acc/tot) + "\n")
    sys.stderr.write("BI recall    = " + str(tp_bi/tot_rec_bi) + "\n")
    if tot_prec_bi > 0:
        sys.stderr.write("BI precision = " + str(tp_bi/tot_prec_bi) + "\n")
    sys.stderr.write("O recall     = "     + str(tp_o/tot_rec_o) + "\n")
    if tot_prec_o > 0:
        sys.stderr.write("O precision  = "  + str(tp_o/tot_prec_o) + "\n\n")

if __name__ == "__main__":
    testfile = sys.argv[1]
    weightsfile = sys.argv[2]
    gazfile = sys.argv[3]
    brownfile = sys.argv[4]
    sents, goldtagseqs, postagseqs = read_data(testfile)
    info = get_maps(sents, postagseqs, gazfile, brownfile)
    weights = read_weights(weightsfile)
    decode(sents, goldtagseqs, postagseqs, info, weights)

