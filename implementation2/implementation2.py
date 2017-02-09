import sys
import random

def read_file(filename):
    sequences = []

    f = open(filename, 'r')

    #reads the file in as a list of tuples to ease manipulation
    for line in f:
        sequences.append((line.split(',')[0], line.split(',')[1].strip('\n')))

    return sequences

def generate_random_inputs(n):
    rand_seqs = []
    bases = 'ACTG'

    for i in range(10):
        seq1 = ""
        seq2 = ""
        for j in range(n):
            seq1 += random.choice(bases)
            seq2 += random.choice(bases)

        rand_seqs.append((seq1, seq2))

    return rand_seqs


def main():

    print generate_random_inputs(500)

if __name__ == '__main__':
    main()
