#/usr/bin/python

from __future__ import division
from random import shuffle
import sys
import features
from cost_viterbi import execute
from decoder import decode

step = 1.0
all_labels = ['B', 'I', 'O']

def init_weights(all_features):
    fmap = {}
    for feat in all_features:
        fmap[feat]  = 0.0
    return fmap

def run(sentset, labelset, postagset, all_feats, info, weights, testdata):
    tsents, tgoldtagseqs, tpostagseqs, tinfo = testdata

    weights_avg = init_weights(all_feats)
    order = [i for i in range(len(sentset))]
    shuffle(order)
    k = 0
    for j in order:
	sys.stderr.write(str(k)+"\r")
	
	sent = sentset[j]
	labelseq = labelset[j]
	postagseq = postagset[j]

	predseq = execute(sent, all_labels, postagseq, weights, labelseq, info)
	if labelseq != predseq:
	    update(weights, predseq, labelseq, sent, postagseq, info)
	    add_weights(weights_avg, weights)

        k += 1
        if k % 10000 == 0 or k == len(sentset):
            decode(tsents, tgoldtagseqs, tpostagseqs, tinfo, weights)

    for key in weights_avg.iterkeys():
        weights_avg[key] /= len(sentset)
        print key, weights_avg[key]
    print
    
    weights = weights_avg.copy()
    return weights

def add_weights(w1, w2):
    #for i in range(len(w1)):
        #w1[i] += w2[i]
    for i in w1.iterkeys():
        w1[i] += w2[i]
        
def update(weights, predseq, labelseq, sent, postagseq, info):
    for i in range(len(predseq)):
        true = labelseq[i]
        pred = predseq[i]
        pos = postagseq[i]
        if i == 0:
            prev_true = '*'
            prev_pred = '*'
        else:
            prev_true = labelseq[i-1]
            prev_pred = predseq[i-1]
        if true != pred:
            true_feats = features.extract(sent[i], true, prev_true, pos, info)
            pred_feats = features.extract(sent[i], pred, prev_pred, pos, info)
            up = set(true_feats).difference(set(pred_feats))
            for u in up:
                if u in weights:
                    weights[u] += step
            down = set(pred_feats).difference(set(true_feats))
            for d in down:
                if d in weights:
                    weights[d] -= step
    return weights  

def learn_and_decode(trainfile, featlistfile, gazfile, num_iter, testfile):
    sentset, labelset, postagset, all_feats, info = features.get_all(trainfile, gazfile, featlistfile)
    sys.stderr.write("\n" + str(len(all_feats)) + " features in all\n")

    sys.stderr.write("\nreading test data \n")
    tsents, tgoldtagseqs, tpostagseqs = features.read_data(testfile)
    tinfo = features.get_maps(tsents, tpostagseqs, gazfile)
    
    testdata = (tsents, tgoldtagseqs, tpostagseqs, tinfo)
    weights = init_weights(all_feats)
    tot_weights = init_weights(all_feats)
 
    for ite in range(num_iter):
        sys.stderr.write("Iteration " + str(ite) + "\n"+ str(len(sentset)) + " sentences\n")
        weights = run(sentset, labelset, postagset, all_feats, info, weights, testdata)
        add_weights(tot_weights, weights)
        #decode(tsents, tgoldtagseqs, tpostagseqs, tinfo, weights)

    for key in tot_weights.iterkeys():
        tot_weights[key] /= num_iter
        print key, tot_weights[key]
    print

    sys.stderr.write("\nfinal performance on test\n")
    decode(tsents, tgoldtagseqs, tpostagseqs, tinfo, tot_weights)

if __name__ == "__main__":
    trainfile = sys.argv[1]
    featlistfile = sys.argv[2]
    gazfile = sys.argv[3]
    num_iter = int(sys.argv[4])
    testfile = sys.argv[5]

    learn_and_decode(trainfile, featlistfile, gazfile, num_iter, testfile)
