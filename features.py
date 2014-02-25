# /usr/bin/python

import sys, re

'''
2 places for feature type
2 place for label
6 places for word
'''
def extract(word, label, prev, postag, info):
    feats = []
    ftype = 100000000
    ltype = 100000
    vocmap, pmap, tagmap, glist = info

    # 1. bigram
    # feats.append('Li-1='+prev+':Li='+label)
    # one extra feature for stopping/starting probability
    #print 'Li-1='+prev+':Li='+label
    if label in tagmap and prev in tagmap:
        feats.append(1 * ftype + tagmap[prev] * ltype + tagmap[label])
    elif label in tagmap and prev == "*":
        feats.append(1 * ftype + 0 + tagmap[label])
    elif prev in tagmap and label == '<STOP>':
        feats.append(1 * ftype + tagmap[prev] * ltype + 0)
    
    # 2. emission
    # feats.append('Li='+label+':Wi='+word)
    if label in tagmap and word in vocmap:
        feats.append(2 * ftype + tagmap[label] * ltype + vocmap[word])

    # 3. pos tag
    # feats.append('Li='+label+':Pi='+postag)
    if label in tagmap and postag in pmap:
        feats.append(3 * ftype + tagmap[label] * ltype + pmap[postag])

    # 4. is punctuation
    # feats.append('Li='+label+":PUi")
    if label in tagmap and len(word) == 1 and word.isdigit() == False and word.isalnum() == False:
        feats.append(4 * ftype + tagmap[label] * ltype)

    # 5. contains punctuation
    if label in tagmap and word.isalnum() == False:
	#feats.append('Li='+label+":Qi")
        feats.append(5 * ftype + tagmap[label] * ltype)

    # 6. is title-cased
    if label in tagmap and word.istitle():
	#feats.append('Li='+label+":Ti")
        feats.append(6 * ftype + tagmap[label] * ltype)

    # 7. is capitalized
    if label in tagmap and word.isupper():
        #feats.append('Li='+label+":Ui")
        feats.append(7 * ftype + tagmap[label] * ltype)

    # 8. is abbrev - ends with a period
    if label in tagmap and word.endswith('.'):
        #feats.append('Li='+label+":Ai")
        feats.append(8 * ftype + tagmap[label] * ltype)

    # 9. is all in small case
    if label in tagmap and word.islower():
        #feats.append('Li='+label+":Si")
        feats.append(9 * ftype + tagmap[label] * ltype)

    # 10. is a year
    if label in tagmap and word.isdigit() and len(word)==4:
        #feats.append('Li='+label+":Yi")
        feats.append(10 * ftype + tagmap[label] * ltype)
    # 11. is a number
    if label in tagmap and word.isdigit():
        #feats.append('Li='+label+":Di")
        feats.append(11 * ftype + tagmap[label] * ltype)

    # 12. is a plural - ends with an 's'
    if label in tagmap and word.endswith('s'):
        #feats.append('Li='+label+":PLi")
        feats.append(12 * ftype + tagmap[label] * ltype)

    # 13. length is 1
    if label in tagmap and len(word) == 1:
        #feats.append('Li='+label+":Oi")
        feats.append(13 * ftype + tagmap[label] * ltype)

    # 14. contains a '.com'
    if label in tagmap and word.endswith('.com'):
        #feats.append('Li='+label+":Ci")
        feats.append(14 * ftype + tagmap[label] * ltype)

    # 15. contains a number
    if label in tagmap and word.isalpha()==False and word.isalnum()==True:
        #feats.append('Li='+label+":Ni")
        feats.append(15 * ftype + tagmap[label] * ltype)

    # 16. contains a "'s"
    if label in tagmap and "'s" in word:
        #feats.append('Li='+label+":APi")
        feats.append(16 * ftype + tagmap[label] * ltype)

    # 17. gazetteer
    #if glist != None and label in tagmap and word in glist:
        #feats.append(17 * ftype + tagmap[label] * ltype)

#    if feat_list == None:
#        return feats
#    else:
#        feat_indices = []
#        for feat in feats:
#            if feat not in feat_list:
#                continue
#            feat_indices.append(feat_list.index(feat))
#        return feat_indices
    return feats

