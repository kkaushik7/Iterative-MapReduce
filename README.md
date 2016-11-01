This project is an implementation of the computations of the steady state matrix of a Makov Chain in a Map Reduce Framework. The computations are done in an iterative fashion where the output from the reducer is fed back to the mapper until convergence is achieved.

All codes are written in *Python 2.7*

twoStepMarkov.py:
---------------------------------
**Usage**: 'python twoStepMarkov.py [input_file] [output_file]'

This code computes the Steady State matrix using a 2-step matrix multiplication framework. This code runs on a local machine, not a Hadoop cluster.

Consider an nxn Markov Transition Matrix A, the elements of which are represented by A<sub>ij</sub>. Every line of the input file should be of the following format:

i	j	A<sub>ij</sub>  

For example for an I<sub>2</sub> matrix, the input_file will look like:  

1	1	1  
1	2	0  
2	1	0  
2	2	1  

Sample input file provided as 'sampleInputMat.txt'

markovSSmatrix_hadoop.py:
---------------------------------
**Usage**: 'python markovSSmatrix_hadoop.py [input_file] temp.txt'

This code computes the Steady State matrix using a 1-step matrix multiplication framework. Runs on the Cloudera Hadoop Distributed file system. This cannot be run on a local machine. Format of the input file here is the same.