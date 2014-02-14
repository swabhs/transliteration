#! /usr/bin/python

'''
Featurized Viterbi algorithm
Created on Sep 12, 2013

@author: swabha
'''

from features import extract
from collections import defaultdict

def execute(sentence, labelset, postags, weights, goldlabels, info):
    if '*' not in labelset:
        labelset.append('*')
    n = len(sentence)
    pi = []
    bp = []

    #print 'initializing...'
    for i in xrange(0, n+1):
        pi.append(defaultdict())
        bp.append(defaultdict())
        for label in labelset:
            pi[i][label] = float("-inf")
            bp[i][label] = ""
    pi[0]['*'] = 0.0
    
    # print 'main viterbi algorithm ...'
    for k in xrange(1, n+1):
        for u in labelset:
            max_score = float("-inf")
            argmax = '1'
            for w in labelset:
                if k >= 2  and w != goldlabels[k-2]:
                    cost = 1.0
                    if goldlabels[k-2] in ('B','I') and w == 'O':
                        cost += 3.0
                else:
                    cost = 0.0
                local_score, feats = get_score(sentence[k-1], u, w, postags[k-1],  weights, info)
                score = pi[k-1][w] + local_score + cost
                if score > max_score:
                    max_score = score
                    argmax = w
            pi[k][u] = max_score
            bp[k][u] = argmax
            
#            for w in labelset:
#                print "{0:.2f}".format(pi[k][w]) + " ",
#            print 
    
    # print "decoding..."
    tags = []
    
    max_score = float("-inf")
    best_last_label = '1'
    for w in labelset:
        local_score = 0.0 #get_score('<STOP>', w, weights)
        
        score = pi[n][w] + local_score
        if score > max_score:
            max_score = score
            best_last_label = w
    tags.append(best_last_label)

    # tag extraction
    
    for k in range(n-1, 0, -1):
        last_tag = tags[len(tags)-1]
        tags.append(bp[k+1][last_tag])
    
    tags = list(reversed(tags))
    
    return tags

def get_score(word, current_tag, prev_tag, postag, weights, info):
    score = 0.0
    features_list = extract(word, current_tag, prev_tag, postag, info)

    for feature in features_list:
        if feature in weights:
            score += weights[feature]

    return score, features_list

