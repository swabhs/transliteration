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

    acc = 0.0
    tot = 0

    sys.stderr.write("total test sentences = " + str(len(sents)) + "\n")
    for i in range(len(sents)):
        sys.stderr.write(str(i) + "\r")
	sent = sents[i]
        postags = postagseqs[i]

	tags, f = viterbi.execute(sent, labelset, postags, weights, info)
        for j in range(len(tags)):
            if tags[j] == goldtagseqs[i][j]:
                acc += 1
        
        tot += len(tags)
        #print ' '.join(sent)
	#print ' '.join(tags), '\n', ' '.join(tagseqs[i])
        #print
    sys.stderr.write("full acc =" + str(acc/tot) + "\n\n")

if __name__ == "__main__":
    testfile = sys.argv[1]
    weightsfile = sys.argv[2]
    gazfile = sys.argv[3]
    sents, goldtagseqs, postagseqs = read_data(testfile)
    info = get_maps(sents, postagseqs, gazfile)
    weights = read_weights(weightsfile)
    decode(sents, goldtagseqs, postagseqs, info, weights)

