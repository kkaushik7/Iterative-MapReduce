#!/usr/bin/python
# $env:path="$env:Path;C:\Python27"

import sys, re, numpy;


# The First Mapper Function
def mapperOne (inputfile):
	inputmat = open(inputfile,'r')
	mapperOneOut = dict()
	for line in inputmat:
		arr = re.split("[ \t]+", line.strip());
		if arr[0] == 'A':
			(mat,i,j,a_ij) = (arr[0],arr[1],arr[2],arr[3])
			key = j
			value = [str(mat),int(i),float(a_ij)]
			mapperOneOut.setdefault(key, []).append(value)
		else: 
			(mat,j,k,b_jk) = (arr[0],arr[1],arr[2],arr[3])
			key = j
			value = [str(mat),int(k),float(b_jk)]
			mapperOneOut.setdefault(key, []).append(value)
	inputmat.close()		
	return mapperOneOut


# The First Reducer	Function
def reducerOne (mapperOneOut):
	reducerOneOut = dict()
	for key in sorted(mapperOneOut.iterkeys()):
		listA = []
		listB = []		
		outerList = mapperOneOut[key]
		for innerList in outerList:
			if innerList[0] == 'A':
				listA.append((innerList[1],innerList[2]))
			else:
				listB.append((innerList[1],innerList[2]))
		for (i,a_ij) in listA:
			for (k,b_jk) in listB:
				value = [i,k,a_ij * b_jk]
				reducerOneOut.setdefault(key, []).append(value)
	return reducerOneOut

# The Second Mapper Function
def mapperTwo (reducerOneOut):
	mapperTwoOut = dict()
	for key in sorted(reducerOneOut.iterkeys()):
		outerList = reducerOneOut[key]
		for innerList in outerList:
			key = (innerList[0],innerList[1])
			value = innerList[2]
			mapperTwoOut.setdefault(key, []).append(value)
	return mapperTwoOut
	
# The Second Reducer Function
def reducerTwo (mapperTwoOut):
	reducerTwoOut = dict()
	for key in sorted(mapperTwoOut.iterkeys()):
		sum = 0
		value = mapperTwoOut[key]
		for v in value:
			sum += v
		reducerTwoOut[key] = sum
	return reducerTwoOut

	
# This function reads the input file and converts the lines of text into a matrix
def inputToTransitionMatrix(inputfile,n):
	transitionMatrix = numpy.empty([n, n])
	file = open(inputfile,'r')
	for line in file:
		arr = re.split("[ \t]+", line.strip());
		if arr[0] == 'B':
			(i,j,bij) = (float(arr[1]),float(arr[2]),float(arr[3]))
			(i,j,bij) = (int(i),int(j),float(bij))
			transitionMatrix[i-1,j-1] = bij
	return transitionMatrix
	
	
# This function converts a dictionary having [(i,j),Aij] values into a Matrix
def dictToMatrix (MapReduceOut,n):
	mat = numpy.empty([n, n])
	for key in sorted(MapReduceOut.iterkeys()):
		(i,j)=key
		mat[i-1,j-1] = MapReduceOut[key]
	return mat
	
# This function writes the Matrix into a file in the Following Format : A, i, j, Aij
def nextIterMatFile (aMat,bMat,n,outputFile):
	file = open(outputFile,'w')
	for i in xrange(0,n):
		for j in xrange(0,n):
			file.write('A'+'\t'+str(i+1)+'\t'+str(j+1)+'\t'+str(aMat[i,j])+'\n')
	for i in xrange(0,n):
		for j in xrange(0,n):
			file.write('B'+'\t'+str(i+1)+'\t'+str(j+1)+'\t'+str(bMat[i,j])+'\n')
	file.close()
	

# MAIN FUNCTION
if __name__ == '__main__':  

	# The First Matrix Multiplication
	# Input Parameters 
	inputfile = sys.argv[1]
	outFile = sys.argv[2]
	n = int(numpy.sqrt((sum(1 for line in open(inputfile)))/2))
	transMat = inputToTransitionMatrix(inputfile,n)
	
	# Printing Out the Input Parameters
	print '\n The given matrix is a ',n,'x',n,' Matrix'
	print '\n The transition matrix is \n',transMat
	
	#The First MapReduce Operation
	mapperOneOut = mapperOne(inputfile)
	reducerOneOut = reducerOne(mapperOneOut)
	mapperTwoOut = mapperTwo(reducerOneOut)
	reducerTwoOut = reducerTwo(mapperTwoOut)
	
	# Converting the raw output to a matrix format
	newMat = dictToMatrix(reducerTwoOut,n)
	
	# Write the file to a similar file that can be read
	nextIterMatFile (newMat,transMat,n,outFile)	
	
	# Iterative MapReduce
	oldMat = numpy.empty([n, n])
	diffMat = oldMat - newMat
	absDiffMat = numpy.absolute(diffMat)
	i=2
	print '\n The P^',i,' =  \n',newMat
	
	while (absDiffMat.max() >= 0.000000001):
	#for g in xrange(0,25):
		i = i+1
		print i
		oldMat = newMat
		mapperOneOut = mapperOne(outFile)
		reducerOneOut = reducerOne(mapperOneOut)
		mapperTwoOut = mapperTwo(reducerOneOut)
		reducerTwoOut = reducerTwo(mapperTwoOut)
		newMat = dictToMatrix(reducerTwoOut,n)
		print '\n P^',i,' =  \n',newMat
		nextIterMatFile (newMat,transMat,n,outFile)
		diffMat = oldMat - newMat
		absDiffMat = numpy.absolute(diffMat)
		print '\n diffMat=\n', diffMat
		print '\n abs diffMat=\n', numpy.absolute(diffMat)
		
	print '\n The Steady State Matrix is found after',i,'iterations and it is \n', newMat





		