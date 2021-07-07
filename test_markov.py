#!/usr/bin/env python3

import sys
from time import time
from markov import markov_chain

def main(script, filename='cicero.txt', n=100, order=2):
    try:
        n = int(n)
        order = int(order)
    except ValueError:
        print('Usage: %s filename [# of words] [prefix length]' % script)
    else:
        chain = markov_chain(filename, n, order)
        print(chain)

if __name__ == '__main__':
    t1 = time()
    main(*sys.argv)
    t2 = time()
    print('Elapsed time in seconds: %.3f' % (t2 - t1))
