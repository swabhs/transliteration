#/usr/bin/python

from __future__ import division
from random import shuffle
import sys
import framework
from features import extract
from cost_viterbi import execute
from decoder import decode

step = 1.0
all_labels = ['B', 'I', 'O']

def init_weights(all_features):
    fmap = {}
    for feat in all_features:
        fmap[feat]  = 0.0
    return fmap

'''
Runs one iteration of the structured perceptron, cost-augmented
'''
def run(sentset, labelset, postagset, all_feats, info, weights, testdata, ad):
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
	    update(weights, predseq, labelseq, sent, postagseq, info, ad)
	    add_weights(weights_avg, weights)

        k += 1
        if k % 10000 == 0: 
            decode(tsents, tgoldtagseqs, tpostagseqs, tinfo, weights)

    decode(tsents, tgoldtagseqs, tpostagseqs, tinfo, weights)
    return weights_avg, weights

def add_weights(w1, w2):
    for i in w1.iterkeys():
        w1[i] += w2[i]
        
def update(weights, predseq, labelseq, sent, postagseq, info, ad):
    for i in range(len(predseq) + 1):
        if i == len(predseq):
            word = ''
            pos = ''
            true = '<STOP>'
            pred = '<STOP>'
        else:
            word = sent[i]
            true = labelseq[i]
            pred = predseq[i]
            pos = postagseq[i]

        if i == 0:
            prev_true = '*'
            prev_pred = '*'
        else:
            prev_true = labelseq[i-1]
            prev_pred = predseq[i-1]

        if true != pred or i == len(predseq) and prev_true != prev_pred:
            true_feats = extract(word, true, prev_true, pos, info)
            pred_feats = extract(word, pred, prev_pred, pos, info)

            up = set(true_feats).difference(set(pred_feats))
            down = set(pred_feats).difference(set(true_feats))
            # ADAGRAD
            for u in up:
                if u in ad:
                    ad[u] += 1
            for d in down:
                if d in ad:
                    ad[d] += 1
            
            for u in up:
                if u in weights:
                    weights[u] += step/ad[u] # ADAGRAD
            for d in down:
                if d in weights:
                    weights[d] -= step/ad[d] # ADAGRAD
        
    return weights  

def learn_and_decode(trainfile, featlistfile, gazfile, num_iter, testfile):
    sentset, labelset, postagset, all_feats, info = framework.get_all(trainfile, gazfile, featlistfile)
    sys.stderr.write("\n" + str(len(all_feats)) + " features in all\n")

    sys.stderr.write("\nreading test data \n")
    tsents, tgoldtagseqs, tpostagseqs = framework.read_data(testfile)
    tinfo = framework.get_maps(tsents, tpostagseqs, gazfile)
    
    testdata = (tsents, tgoldtagseqs, tpostagseqs, tinfo)
    weights = init_weights(all_feats)
    tot_weights = init_weights(all_feats)
 
    #ADAGRAD
    ad = init_weights(all_feats)

    for ite in range(num_iter):
        sys.stderr.write("Iteration " + str(ite) + "\ntotal train sentences = "+ str(len(sentset)) + "\n")
        weights_a, weights = run(sentset, labelset, postagset, all_feats, info, weights, testdata, ad) #ADAGRAD
        framework.write_weights(weights, ite)
        add_weights(tot_weights, weights_a)

    for key in tot_weights.iterkeys():
        tot_weights[key] /= num_iter*len(sentset)

    sys.stderr.write("\n\nfinal performance on test\n")
    decode(tsents, tgoldtagseqs, tpostagseqs, tinfo, tot_weights)

if __name__ == "__main__":
    trainfile = sys.argv[1]
    featlistfile = sys.argv[2]
    gazfile = sys.argv[3]
    num_iter = int(sys.argv[4])
    testfile = sys.argv[5]

    learn_and_decode(trainfile, featlistfile, gazfile, num_iter, testfile)
