# /usr/bin/python

import sys

'''
Reads the output of mnt.py and tries to make
labeled data for training
'''

def read_data(filename):
    f = open(filename, "r")
    while True:
        line = f.readline()
        if not line:
            break
        line = line.strip()
        sent, tagseq = line.split(' ||| ')
        sentence = sent.split(' ')
        tags = tagseq.split(' ')
        if len(sentence) != len(tags):
            sys.stderr.write(sent+ " "+ tagseq + "\n")
            continue
        i = 0
        for word in sentence:
            tag = tags[i]
#            if tags[i] == "B" or tags[i] == "I":
#                tag = "1"
#            else:
#                tag = "0"
            print word+"\t"+tag
            i += 1
        print
    f.close()

if __name__ == "__main__":
    read_data(sys.argv[1])
