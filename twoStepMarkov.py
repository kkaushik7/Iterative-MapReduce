#!/usr/bin/python
# $env:path="$env:Path;C:\Python27"

import sys, re, numpy;

#Mapper
def mapper (inputfile):
	inputmat = open(inputfile,'r')
	mapperOneOut = dict()
	N = int(numpy.sqrt((sum(1 for line in open(inputfile)))/2))
	for line in inputmat:
		arr = re.split("[ \t]+", line.strip());
		if arr[0] == 'A':
			(mat,i,j,a_ij) = (arr[0],arr[1],arr[2],arr[3])
			for k in xrange(1,N+1):
				key = (int(i),int(k))
				value = [str(mat),int(j),float(a_ij)]
				mapperOneOut.setdefault(key, []).append(value)
		else: 
			(mat,j,k,b_jk) = (arr[0],arr[1],arr[2],arr[3])
			for i in xrange(1,N+1):
				key = (int(i),int(k))
				value = [str(mat),int(j),float(b_jk)]
				mapperOneOut.setdefault(key, []).append(value)
	inputmat.close()		
	return mapperOneOut

# Reducer
def reducer (mapperOut):
	reducerOut = dict()
	for key in sorted(mapperOut.iterkeys()):
		value = 0
		listA = []
		listB = []
		outerList = mapperOut[key]
		for innerList in outerList:
			if innerList[0] == 'A':
				listA.append((innerList[1],innerList[2]))
			else:
				listB.append((innerList[1],innerList[2]))
		for (j,a_ij) in listA:
			for (J,b_jk) in listB:
				if (j==J):
					value += a_ij*b_jk
		reducerOut[key] = value
	return reducerOut

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

	
# Main
if __name__ == '__main__':  
	file = sys.argv[1]
	n = int(numpy.sqrt((sum(1 for line in open(file)))/2))
	transMat = inputToTransitionMatrix(file,n)
	print '\n The given ',n,' x ',n,' matrix is \n', transMat
	oldMat = numpy.empty([n, n])
	newMat = dictToMatrix(reducer(mapper(file)),n)
	diffMat = numpy.absolute(oldMat - newMat)
	nextIterMatFile (newMat,transMat,n,file)	
	i=1
	while (diffMat.max() >= 0.000000001):
		i += 1
		print '\n P^',i,' =  \n',newMat
		oldMat = newMat
		newMat = dictToMatrix(reducer(mapper(file)),n)
		diffMat = numpy.absolute(oldMat - newMat)
		nextIterMatFile (newMat,transMat,n,file)
	print '\n The Steady State Matrix is found after',i,'iterations and it is \n', newMat