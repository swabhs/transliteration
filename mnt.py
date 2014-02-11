import sys, re

nostarts = set()
noends = set()
for p in ['(', '[', ':', ';', '.', ',', '"', '\'', '?', '-', '--', 'in', 'In', 'IN', 'am', 'Am', 'An', 'an', 'AN', 'AM', 'so', 'was', 'So', 'Was']:
  nostarts.add(p)
  noends.add(p)
nostarts.add('!')
nostarts.add('%')
nostarts.add(')')
nostarts.add(']')
noends.add('$')
allpuncs = nostarts.union(nostarts)

# things that need to be handled:
# 'Richard - Strauss - Strasse ||| Richard Strass Strasse' should probably be tagged as B I I I I rather than B O B O B
# 12,5 % ||| 12.5 %

def build_match_trie(words):
  s=len(words)
  t = {}
  for i in range(s):
    d = t
    prefix = set()
    for j in range(i,s):
      if j - i < 20:
        w=words[j]
        if w == ',': break
        prefix.add(w)
        if w in d:
          d = d[w]
        else:
          score = 2 ** (j-i)
          # print words[i:j+1],score  #DEBUG
          if (w in noends): score = 0
          if (w == ')' and not '(' in prefix): score = 0
          if (w == ']' and not '[' in prefix): score = 0
          if (words[i] in nostarts): score = 0
          if (score == 1 and w in allpuncs): score = 0
          d[w] = {'__SCORE':score}
          d = d[w]
  return t

#for line in sys.stdin:
f = open(sys.argv[1], "r")
while True:
  line = f.readline()
  if not line:
    break
  line = line.strip()
  (sfr, sen, al) = line.split(' ||| ')
  ens = sen.lower().split()
  trie = build_match_trie(ens)
  frs = sfr.lower().split()
  chart = [(0.0, None, 0) for x in frs]
  chart.append((0.0, None, 0, 0.0))
  s = len(frs)
  for i in range(s):
    t = trie
    score = chart[i][0]
    j = i
    matched = 0
    while (j < s and frs[j] in t):
      t = t[frs[j]]
      j += 1
      matched += 1
      value = t['__SCORE']
      newscore = value + score
      if newscore > chart[j][0]:
        chart[j] = (newscore, i, matched, value)

    # deal with the no match case
    if (matched == 0):
      newscore = score + 1.0
      if newscore > chart[i+1][0]:
        chart[i+1] = (newscore, i, 0, 0.0)

  j = s
  i = s
  out = []
  while chart[j][1] is not None:
    i = chart[j][1]
    if (chart[j][2] == 0):
      assert(j - i == 1) #DEBUG
      out.append('O')
    else:
      if (chart[j][3] < 1.0):
        for k in range(j - i):
          out.append('O')
      else:
        # sys.stderr.write('%s\n' % ' '.join(frs[i:j]))
        for k in range(j - i - 1):
          out.append('I')
        out.append('B')
    j = i
  out.reverse()
  print sfr,'|||',' '.join(out)


