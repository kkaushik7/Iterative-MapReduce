This code runs the computations of the steady state matrix of a Makov Chain in a Map Reduce Framework. The output from the reducer is fed back to the mapper until convergence is achieved.

This code is written in Python 2.7

Usage: python markov.py [input_file] [output_file]

Format of the input file:
---------------------------------

Consider an nxn Markov Transition Matrix A, the elements of which are represented by Aij. Every line of the input file should be of the following format:

i	j	Aij 

For example for an I2 matrix, the input_file will look like:

1	1	1
1	2	0
2	1	0
2	2	1