import sys
import random
import numpy as np

def read_input_file(filename):
    sequences = []

    f = open(filename, 'r')

    #reads the file in as a list of tuples to ease manipulation
    for line in f:
        sequences.append((line.split(',')[0], line.split(',')[1].strip('\n')))

    return sequences

def build_cost_dict(filename):

    #dictionary of dictionaries that will hold the cost matrix
    cost_dict = {}

    f = open(filename, 'r')

    lines = f.readlines()

    #iterate over each row in the matrix
    for line_iter in range(len(lines)):

        #clean commas and newline characters off of the line
        curr_line = lines[line_iter].replace(',', '').strip('\n')

        #iterate over each character in the line
        for char_iter in range(len(curr_line)):

            #we aren't interested in the first column, we have that info already
            if char_iter != 0:

                #the first line contains the alphabet so use the char as a key to another dictionary
                if line_iter == 0:
                    first_line = curr_line
                    cost_dict[first_line[char_iter]] = {}
                else:
                    #set keys and values for cost_dict's sub dictionaries
                    cost_dict[first_line[char_iter]][curr_line[0]] = int(curr_line[char_iter])

    return cost_dict

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

def unweighted_edit_dist(string_one, string_two):

    m = len(string_one) + 1
    n = len(string_two) + 1

    dist_table = np.zeros((n, m), dtype=int)

    for i in range(m):
        dist_table[0][i] = i

    for j in range(n):
        dist_table[j][0] = j

    for i in range(1, n):
        for j in range(1, m):

            if string_one[i - 1] == string_two[j - 1]:
                diff = 0
            else:
                diff = 2

            dist_table[j][i] = min( dist_table[j][i - 1] + 1,
                                    dist_table[j - 1][i] + 1,
                                    dist_table[j - 1][i - 1] + diff )

    print dist_table
    return dist_table[j][i]

def unweighted_edit_dist_bt(string_one, string_two):

    #representations a few special characters
    diag = 'G'
    left = 'L'
    down = 'D'
    del_char = '-'

    m = len(string_one) + 1
    n = len(string_two) + 1

    #initialize the backtrace and distance tables
    ptr = [['']*m for _ in range(n)]
    dist_table = np.zeros((n, m), dtype=int)

    #set the base column values for the distance table
    for i in range(m):
        dist_table[0][i] = i

    #set the base row values for the distance table
    for j in range(n):
        dist_table[j][0] = j

    #iterate over the entire table
    for i in range(1, n):
        for j in range(1, m):

            #if the characters are the same there is no cost, otherwise a substiution occurs
            if string_one[i - 1] == string_two[j - 1]:
                diff = 0
            else:
                diff = 2

            #get the minimum of our three options for alignment and store it
            dist = min( dist_table[j][i - 1] + 1,
                        dist_table[j - 1][i] + 1,
                        dist_table[j - 1][i - 1] + diff )

            #set the value of the distance table at our current place
            dist_table[j][i] = dist

            #build the back trace table
            if dist == dist_table[j - 1][i - 1] + diff:     #ALIGN-move diag
                ptr[j][i] += diag
            elif dist == dist_table[j][i - 1] + 1:          #DELETE-move down
                ptr[j][i] += down
            elif dist == dist_table[j - 1][i] + 1:          #INSERT-move left
                ptr[j][i] += left

    k = len(string_one)
    l = len(string_two)
    new_str_one = ''
    new_str_two = ''

    #perform the backtrace by starting in the top right corner and following the directions
    while k > 0 and l > 0:
        if ptr[l][k] == diag:
             new_str_one = string_one[k - 1] + new_str_one
             new_str_two = string_two[l - 1] + new_str_two

             k -= 1
             l -= 1

        elif ptr[l][k] == left:
            new_str_one = del_char + new_str_one
            new_str_two = string_two[l - 1] + new_str_two

            l -= 1

        elif ptr[l][k] == down:
            new_str_one = string_one[k - 1] + new_str_one
            new_str_two = del_char + new_str_two

            k -= 1

    #this conditional covers the case where one index reached zero before the other
    if k > 0:
        for x in range(k, 0, -1):
            new_str_one = string_one[x - 1] + new_str_one
            new_str_two = del_char + new_str_two
    elif l > 0:
            new_str_one = del_char + new_str_one
            new_str_two = string_two[x - 1] + new_str_two

    return dist_table[j][i], new_str_one, new_str_two

def main():

    str1 = 'INTENTION'
    str2 = 'EXECUTION'

    dist, newstr1, newstr2 = weighted_edit_dist_bt(str1, str2)

    print dist
    print newstr1
    print newstr2

if __name__ == '__main__':
    main()
