#!/usr/bin/env python

#SBATCH --partition=short
#SBATCH --job-name=demult_part1
#SBATCH --time=0-12:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=7
#SBATCH --mail-user=annalundberg92@gmail.com
#SBATCH --mail-type=BEGIN,END,FAIL

import numpy as np
import argparse
import gzip

def get_arguments():
    parser = argparse.ArgumentParser(description="reads fasta file, stores gene id in dict")
    parser.add_argument("-f", "--filename", help="name of file",\
                        required=True, type=str)
    parser.add_argument("-t", "--type", help="index or seq",\
                        required=True, type=str)
    return parser.parse_args()

def convert_phred(letter):
    """(string)->int
    Converts a single character into a phred score"""
    phred = ord(letter)-33
    return phred

def populate_array(file, typ):
    '''(string, string)-> array
    Function opens fastq file, converts phred quality score, adds up q scores of
    each position, stores in array mean_scores, divides mean_scores by number
    of reads to return an array of mean phred scores per position'''
    p_scores = []
    ct = 0
    if typ == 'index': #file contain index reads, seq length will be 8
        num = 8
    elif typ == 'seq': #file contains sequence reads, seq length will be 101
        num = 101
    else: #there was a mistake?
        print('Not a valid type')
    while ct < num: #generate a list of appropriate length
        p_scores.append(0.0)
        ct += 1
    with gzip.open(file,'rt') as f: #open a gzipped file in non-binary read mode
        LN = 0 #init line count
        for line in f:
            LN+=1 #line counter increment
            line = line.strip('\n') #strip newline character
            if LN%4 == 0: #this line is quality scores
                pos = 0
                for ch in line: #look at each score, one at a time
                    qscore = convert_phred(ch) #convert phred score
                    p_scores[pos]+= qscore #append to list
                    pos += 1
        mean_scores=np.array(p_scores)
        reads = LN//4
        mean_scores = mean_scores/reads
    return mean_scores, num

def main():
    '''run all the fxns'''
    args = get_arguments()
    print(args.filename)
    mean_phred, num_scores = populate_array(args.filename, args.type)
    print(mean_phred)
    return mean_phred

main()
