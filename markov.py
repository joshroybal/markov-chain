from random import randint, choice
from bisect import bisect_left

def cumsum(t):
    cumulative_sums = []
    acc = 0
    for freq, word in t:
        cumulative_sums.append(acc + freq)
        acc += freq
    return cumulative_sums

def process_file(filename, n):
    t = []
    fin = open(filename, 'r')
    for line in fin:
        process_line(line, t)
    fin.close()
    prefixes = [ tuple(t[i:i+n]) for i in range(len(t)-n) ]
    suffix_map = {}
    for idx, val in enumerate(prefixes[:-1]):
        suffix = prefixes[idx+1][-1] 
        if val not in suffix_map:
            suffix_map[val] = { suffix: 1 }
        else:
            suffix_map[val][suffix] = suffix_map[val].get(suffix, 0) + 1
    prefixes = [ prefix for prefix in prefixes if prefix[0][0].isupper() ]
    endings = [ word for word in t if word[0].islower() and word[-1] == '.' ]
    return prefixes, suffix_map, endings
    
def process_line(line, t):
    line = line.replace('-', ' ')
    t.extend([ word for word in line.split() ])

def markov_chain(filename, no_words, order):
    prefixes, suffix_map, endings = process_file(filename, order)
    prefix = choice(prefixes)
    chain = [ word for word in prefix ]
    while True:
        suffix = choose_random_suffix(suffix_map, prefix)
        chain.append(suffix)
        if len(chain) >= no_words - 1:
            break
        prefix = prefix[1:] + (suffix,)
    chain[-1] = choice(endings)
    count = 0
    for idx, val in enumerate(chain):
        count += len(chain[idx])
        if count >= 78:
            chain[idx-1] += '\n'
            count = len(val)
        else:
            chain[idx-1] += ' '
            count += 1
    text = ''.join(chain)
    return text

def choose_random_suffix(d, prefix):
    t = [ (d[prefix][x], x) for x in d[prefix] ]
    suffix = weighted_binary_search(t)
    return suffix

def weighted_binary_search(t):
    t.sort(reverse=True)
    acc_sums = cumsum(t)
    idx = randint(1, acc_sums[-1])
    pos = bisect_left(acc_sums, idx)
    return t[pos][1]
