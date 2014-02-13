#/usr/bin/python

from __future__ import division
import features, sys
from cost_viterbi import execute

step = 1.0
all_labels = ['B', 'I', 'O']

def init(all_features):
    fmap = {}
    for feat in all_features:
        fmap[feat] = 0.0
        
    return fmap

def run(sentset, labelset, postagset, num_iter, all_feats, k):
    weights = init(all_feats)
    weights_avg = init(all_feats)

    for i in range(num_iter):
        sys.stderr.write("Iteration " + str(i) + "\n"+ str(len(sentset)) + " sentences\n")
        for j in range(len(sentset)/k):
            sys.stderr.write(str(j)+"\r")
            
            sent = sentset[j]
            labelseq = labelset[j]
            postagseq = postagset[j]
            
            predseq, f = execute(sent, all_labels, postagseq, weights, labelseq)
            if labelseq != predseq:
                update(weights, predseq, labelseq, sent, postagseq)
                add_weights(weights_avg, weights)

    for f in weights_avg.iterkeys():
        weights_avg[f] /= num_iter*len(sentset)
        print f, weights_avg[f]
    return weights_avg
        
def update(weights, predseq, labelseq, sent, postagseq):
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
            true_feats = features.extract(sent[i], true, prev_true, "_")
            for feat in true_feats:
                if feat in weights:
                    weights[feat] += step
            pred_feats = features.extract(sent[i], pred, prev_pred, "_")
            for feat in pred_feats:
                if feat in weights:
                    weights[feat] -= step
    return weights  

#TODO array instead of map
def add_weights(wmap1, wmap2):
    for f in wmap1.iterkeys():
        wmap1[f] += wmap2[f]

if __name__ == "__main__":
    sentset, labelset, postagset, all_feats = features.get_all(sys.argv[1])
    sys.stderr.write("\n" + str(len(all_feats)) + " features in all\n")
    num_iter = 1
    frac = int(sys.argv[2])
    run(sentset, labelset, postagset, num_iter, all_feats, frac)
