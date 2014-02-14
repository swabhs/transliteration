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
    vocmap, pmap, tagmap = info

    # 1. bigram
    # feats.append('Li-1='+prev+':Li='+label)
    if label in tagmap and prev in tagmap:
        feats.append(1 * ftype + tagmap[prev] * ltype + tagmap[label])
    
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

def read_features(featsfile):
    featlist = []
    feats = open(featsfile, 'r')
    while True:
        line = feats.readline()
        if not line:
            break
        featlist.append(int(line.strip()))
    feats.close()
    return featlist
    
def extract_all_train_features(sents, tagseqs, postagseqs, info):
    featset = set([])
    i = 0
    for sent in sents:
        sys.stderr.write(str(i) + "\r")
        j = 0
        for word in sent:
            tag = tagseqs[i][j]
            postag = postagseqs[i][j]
            if j == 0: # first position
               prev = '*'
            else:
               prev = tagseqs[i][j-1]
            featset.update(extract(word, tag, prev, postag, info)) # get a list of all features possible
            j += 1
        i += 1
    featlist = list(featset)
    for f in featlist:
        print f
    return featlist

def read_data(datafile):
    data = open(datafile, 'r')
    sents = []
    tagseqs = []
    postagseqs = []
    sent = []
    tags = []
    postags = []
    while 1:
        line = data.readline()
        if not line:
	   break
        line = line.strip()
	if line == "":
	    sents.append(sent)
	    tagseqs.append(tags)
	    postagseqs.append(postags)
	    sent = []
	    tags = []
	    postags = []
	    continue
        
	word, pos, tag = line.split("\t")
	sent.append(word.strip())
	tags.append(tag.strip())
	postags.append(pos.strip())
    data.close()
    return sents, tagseqs, postagseqs

def get_maps(sents, tagseqs, postagseqs):
    vocset = set([])
    pset = set([])

    for sent in sents:
        vocset.update(sent)
    for postags in postagseqs:
        pset.update(postags)

    voclist = list(vocset)
    plist = list(pset)

    i = 1
    vocmap = {}
    for wtype in voclist:
        vocmap[wtype] = i
        i += 1

    j = 1
    pmap = {}
    for ptype in plist:
        pmap[ptype] = j
        j += 1

    lmap = {'B':1, 'I':2, 'O':3}
    return (vocmap, pmap, lmap) 

def get_all(trainfile):
    sys.stderr.write("reading training data\n")
    sents, tagseqs, postagseqs = read_data(trainfile)
    info = get_maps(sents, tagseqs, postagseqs)
    
    sys.stderr.write("extracting features from " + str(len(sents)) + " sentences\n")
    #featlist = extract_all_train_features(sents,tagseqs, postagseqs, info)
    featlist = read_features(sys.argv[2])

    return sents, tagseqs, postagseqs, featlist, info

if __name__ == "__main__":
    #sentset, labelset, postagset = read_data(sys.argv[1])
    sentset, labelset, postagset, all_feats, info = get_all(sys.argv[1])
    #print len(sentset)
    #print len(labelset)
    #print len(all_feats)
