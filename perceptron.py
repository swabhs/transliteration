#/usr/bin/python

from __future__ import division
import sys
import features
from cost_viterbi import execute

step = 1.0
all_labels = ['B', 'I', 'O']

def init_weights(all_features):
    fmap = {}
    for feat in all_features:
        fmap[feat]  = 0.0
    return fmap

def run(sentset, labelset, postagset, num_iter, all_feats, info):
    weights = init_weights(all_feats)
    weights_avg = init_weights(all_feats)

    for i in range(num_iter):
        sys.stderr.write("Iteration " + str(i) + "\n"+ str(len(sentset)) + " sentences\n")
        for j in range(len(sentset)):
            sys.stderr.write(str(j)+"\r")
            
            sent = sentset[j]
            labelseq = labelset[j]
            postagseq = postagset[j]
            predseq = execute(sent, all_labels, postagseq, weights, labelseq, info)
            if labelseq != predseq:
                update(weights, predseq, labelseq, sent, postagseq, info)
                add_weights(weights_avg, weights)

#    for i in range(len(weights_avg)):
#        weights_avg[i] /= num_iter*len(sentset)
#    for f in all_feats:
#        print f, weights_avg[all_feats.index(f)]
    for i in weights_avg.iterkeys():
        weights_avg[i] /= num_iter*len(sentset)
        print i, weights_avg[i]
    return weights_avg

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

if __name__ == "__main__":
    sentset, labelset, postagset, all_feats, info = features.get_all(sys.argv[1])
    sys.stderr.write("\n" + str(len(all_feats)) + " features in all\n")
    num_iter = 1
    run(sentset, labelset, postagset, num_iter, all_feats, info)
