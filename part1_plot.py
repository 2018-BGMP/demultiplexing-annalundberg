#!/usr/bin/env python
'''Handle slurm output from part 1 and turn into plot'''

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

def read_slurm(file):
    '''(file)->list,string
    Clean slurm output and extract list of mean phred scores output from
    slurm and filename without path'''
    array=''
    ln=0
    noise=['[', ' ', ']'] #list of characters with data, separating values we want
    item=''
    my_list=[] #init output list
    name = '' #init output filename
    with open(file) as f:
        for line in f:
            line = line.strip('\n') #remove newlines
            if ln==0: # 1st line in file has filename with path
                ln=1
                fname=line #filepath/filename
            else:
                array+=line
    for i in fname: #build file name without file path
        if i == '/':
            name = ''
        elif i == '.':
            break
        else:
            name+=i
    for ch in array:
        if ch in noise:
            if item!='':
                value=float(item)
                my_list.append(value)
                item=''
        else:
            item+=ch
    return my_list, name

def plot_phred(phred_array, nscores, fname):
    '''(numpy array, int) -> filename
    This fxn takes an array representing mean phred scores per position, plots
    mean phred scores, saves plot as a file, which fxn returns name of'''
    plt.plot(range(nscores), phred_array, marker = 'o', linestyle= 'None')
    plt.title('Phred Quality Scores')
    plt.xlabel('Sequence position')
    plt.ylabel('Mean quality score')
    fig_name = fname+'_plot.png'
    plt.savefig(fig_name)
    plt.clf()
    return fig_name

def plot_combine():
    '''This fxn uses slurm extract info fxn to generate 4 sets of names
    and mean phred score lists to build 4 sets of plots using plot_phred fxn'''
    f_list=[]
    files = ['slurm-2111200.out', 'slurm-2111202.out', 'slurm-2111204.out', 'slurm-2111205.out']
    for file in files:
        phred_list, fname = read_slurm(file)
        n = len(phred_list)
        fig = plot_phred(phred_list, n, fname)
        f_list.append(fig)
    return f_list

print(plot_combine())
