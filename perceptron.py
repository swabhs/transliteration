#/usr/bin/python

from __future__ import division
import features, sys
from viterbi import execute

step = 1.0
all_labels = ['B', 'I', 'O']

def init(all_features):
    fmap = {}
    for feat in all_features:
        fmap[feat] = 0.0
        
    return fmap

def run(sentset, labelset, num_iter, all_feats):
    weights = init(all_feats)
    weights_avg = init(all_feats)

    for i in range(num_iter):
        sys.stderr.write(str(i)+"\r")
        for j in range(len(sentset)):
            sent = sentset[j]
            labelseq = labelset[j]
            #postagseq = postagseqs[j]
            predseq, f = execute(sent, all_labels, weights)
            if labelseq != predseq:
                update(weights, predseq, labelseq, sent)
                add_weights(weights_avg, weights)
    for f in weights_avg.iterkeys():
        weights_avg[f] /= num_iter*len(sentset)
        print f, weights_avg[f]
    return weights_avg
        
def update(weights, predseq, labelseq, sent):
    for i in range(len(predseq)):
        true = labelseq[i]
        pred = predseq[i]
        #pos = postagseq[i]
        if i == 0:
            prev_true = '*'
            prev_pred = '*'
        else:
            prev_true = labelseq[i-1]
            prev_pred = predseq[i-1]
        if true != pred:
            #TODO implement trigram
            true_feats = features.extract(sent[i], true, prev_true, "_")
            for feat in true_feats:
                if feat in weights:
                    weights[feat] += step
            pred_feats = features.extract(sent[i], pred, prev_pred, "_")
            for feat in pred_feats:
                if feat in weights:
                    weights[feat] -= step
    return weights  

def add_weights(wmap1, wmap2):
    for f in wmap1.iterkeys():
        wmap1[f] += wmap2[f]

if __name__ == "__main__":
    sentset, labelset, all_feats = features.get_all(sys.argv[1])
    sys.stderr.write(str(len(all_feats)) + "\n")
    num_iter = 50
    run(sentset, labelset, num_iter, all_feats)
