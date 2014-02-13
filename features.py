# /usr/bin/python

import sys, re

def extract(word, label, prev, postag, feat_list):
    feats = []

    # bigram
    feats.append('Li-1='+prev+':Li='+label)
    # trigram
    # feats.append('Li-2='+prevprev+':Li-1='+prev+':Li='+label) 
    # emission
    feats.append('Li='+label+':Wi='+word)
    # pos tag
    feats.append('Li='+label+':Pi='+postag)
    # is punctuation
    if len(word) == 1 and word.isdigit() == False and word.isalnum() == False:
	feats.append('Li='+label+":PUi")
    # contains punctuation
    if word.isalnum() == False:
	feats.append('Li='+label+":Qi")
    # is title-cased
    if word.istitle():
	feats.append('Li='+label+":Ti")
    # is capitalized
    if word.isupper():
        feats.append('Li='+label+":Ui")
    # is abbrev - ends with a period
    if word.endswith('.'):
        feats.append('Li='+label+":Ai")
    # is all in small case
    if word.islower():
        feats.append('Li='+label+":Si")
    # is a year
    if word.isdigit() and len(word)==4:
        feats.append('Li='+label+":Yi")
    # is a number
    if word.isdigit():
        feats.append('Li='+label+":Di")
    # is a plural - ends with an 's'
    if word.endswith('s'):
        feats.append('Li='+label+":PLi")
    # length is 1
    if len(word) == 1:
        feats.append('Li='+label+":Oi")
    # contains a '.com'
    if word.endswith('.com'):
        feats.append('Li='+label+":Ci")
    # contains a number
    if word.isalpha()==False and word.isalnum()==True:
        feats.append('Li='+label+":Ni")
    # contains a "'s"
    if "'s" in word:
        feats.append('Li='+label+":APi")

    if feat_list == None:
        return feats
    else:
        feat_indices = []
        for feat in feats:
            if feat not in feat_list:
                continue
            feat_indices.append(feat_list.index(feat))
        return feat_indices

def get_all(trainfile):
    sys.stderr.write("reading training data\n")
    sents, tagseqs, postagseqs = read_data(trainfile)
    
    sys.stderr.write("extracting features from " + str(len(sents)) + " sentences\n")
    #featlist = extract_all_train_features(sents,tagsseqs, postagseqs
    featlist = read_features(sys.argv[2])

    return sents, tagseqs, postagseqs, featlist

def read_features(featsfile):
    featlist = []
    feats = open(featsfile, 'r')
    while True:
        line = feats.readline()
        if not line:
            break
        featlist.append(line.strip())
    feats.close()
    return featlist
    
def extract_all_train_features(sents, tagseqs, postagseqs):
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
            featset.update(extract(word, tag, prev, postag, None)) # get a list of all features possible
            j += 1
        i += 1
    featlist = list(featset)
    #print '\n'.join(featlist)
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

if __name__ == "__main__":
    #sentset, labelset, postagset = read_data(sys.argv[1])
    sentset, labelset, postagset, all_feats = get_all(sys.argv[1])
    #print len(sentset)
    #print len(labelset)
    #print len(all_feats)
