# /usr/bin/python

from __future__ import division
import viterbi
from features import read_data
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
        weights[f] = float(wt)
    feats.close()
    return weights

def main(testfile, weightsfile):
    labelset = ['B', 'I', 'O', '*']
    sents, goldtagseqs, postagseqs = read_data(testfile)
    weights = read_weights(weightsfile)

    acc = 0.0
    tot = 0

    sys.stderr.write("total test sentences = " + str(len(sents)) + "\n")
    for i in range(len(sents)):
        sys.stderr.write(str(i) + "\r")
	sent = sents[i]
        postags = postagseqs[i]

	tags, f = viterbi.execute(sent, labelset, postags, weights)
        for j in range(len(tags)):
            if tags[j] == goldtagseqs[i][j]:
                acc += 1
        
        tot += len(tags)
        #print ' '.join(sent)
	#print ' '.join(tags), '\n', ' '.join(tagseqs[i])
        #print
    print "full acc =", acc/tot

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

