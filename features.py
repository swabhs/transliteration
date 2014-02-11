# /usr/bin/python

import sys, re

def extract(word, label, prev, prevprev):
    feats = []
    # bigram
    feats.append('Li-1='+prev+':Li='+label)
    # trigram
    feats.append('Li-2='+prevprev+':Li-1='+prev+':Li='+label) 
    # emission
    feats.append('Li='+label+':Wi='+word)
    # pos tag

    # is punctuation
    if len(word) == 1 and word.isdigit() == False and word.isalnum() == False:
	feats.append('Li='+label+":Pi")
    # contains punctuation
    #if len(word) > 1 and re.search('[,.@#\%(){}<>\?!:$\*&\\\-\'\"]', word)!=None:
	#feats.append('Li='+label+":Qi")
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
    return feats

def get_all(trainfile):
     train = open(trainfile, 'r')
     feats = set([])
     sents = []
     tagseqs = []
     #postagseqs = []
     sent = []
     tags = []
     #postags = []
     while 1:
        line = train.readline()
        if not line:
            break
        line = line.strip()
        if line == "":
            sents.append(sent)
            tagseqs.append(tags)
            #postagseqs.append(postags)
            sent = []
            tags = []
            #postags = []
            continue
        word, tag = line.split("\t")
        sent.append(word.strip())
        tags.append(tag.strip())
        #postags.append(pos.strip())
        
        if len(tags) == 1:
            prev = '*'
            prevprev = '*'
        elif len(tags) == 2:
            prevprev = '*'
            prev = tags[-2]
        else:
            prevprev = tags[-3]
            prev = tags[-2]
        #feats.update(extract(word, tag, prev, pos, v1, v2))
        feats.update(extract(word, tag, prev, prevprev))
     #print feats
     train.close()
     #return sents, tagseqs, postagseqs, vecs1, vecs2, list(feats)
     return sents, tagseqs, list(feats)

if __name__ == "__main__":
    sentset, labelset, all_feats = get_all(sys.argv[1])
    print sentset[25]
    print labelset[25]
    print len(all_feats)
