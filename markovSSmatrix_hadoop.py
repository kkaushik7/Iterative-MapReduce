#!/usr/bin/python 
# $env:path="$env:Path;C:\Python27"
# input = inputmatrix.txt
# output is present in output.txt 
 
import sys, re, numpy, dumbo

# This function converts a dictionary having [(i,j),Aij] values into a Matrix
def dictToMatrix (n):
    inputmat = open("outputfile.txt",'r') 
    mat = numpy.empty([n, n])
    for line in inputmat:
        arr = re.split("[ \t]+", line.strip())
        (i,j),a_ij = eval(arr[0]+arr[1]),float(arr[2])
        mat[i-1,j-1] = a_ij
    inputmat.close()
    return mat

# This function reads the input file and converts the lines of text into a matrix 
def inputToTransitionMatrix():
    inputmat = open("inputmatrix.txt",'r')
    n = int(numpy.sqrt((sum(1 for line in open("inputmatrix.txt")))/2)) 
    transitionMatrix = numpy.empty([n, n]) 
    for line in inputmat: 
        arr = re.split("[ \t]+", line.strip()); 
        if arr[0] == 'B': 
            (i,j,bij) = (float(arr[1]),float(arr[2]),float(arr[3])) 
            (i,j,bij) = (int(i),int(j),float(bij)) 
            transitionMatrix[i-1,j-1] = bij
    inputmat.close() 
    return transitionMatrix, n

# This function writes the Matrix into a file in the Following Format : A, i, j, Aij 
def nextIterMatFile (aMat,bMat,n): 
    file = open('inputmatrix.txt','w') 
    for i in xrange(0,n): 
        for j in xrange(0,n): 
            file.write('A'+'\t'+str(i+1)+'\t'+str(j+1)+'\t'+str(aMat[i,j])+'\n') 
    for i in xrange(0,n): 
        for j in xrange(0,n): 
            file.write('B'+'\t'+str(i+1)+'\t'+str(j+1)+'\t'+str(bMat[i,j])+'\n') 
    file.close()

# Function to compute the absolute difference between two matrices and get the maximum value out of it
def maxValueDiff (a, b, n):
        maxi = 0
        for i in xrange(0,n):
            for j in xrange(0,n):
                if a[i,j] - b[i,j] > maxi or b[i,j] - a[i,j] > maxi:
                    if a[i,j] - b[i,j] > b[i,j] - a[i,j]:
                        maxi = a[i,j] - b[i,j]
                    else:
                        maxi = b[i,j] - a[i,j]
    return maxi

#Mapper 
def mapper (key,value): 
    N = int(numpy.sqrt((sum(1 for line in open("inputmatrix.txt")))/2)) 
    arr = re.split("[ \t]+", value.strip()); 
    if arr[0] == 'A': 
        (mat,i,j,a_ij) = (arr[0],int(arr[1]),arr[2],arr[3]) 
        for k in range(1,N+1):
            val = [str(mat), int(j), float(a_ij)] 
            yield (i,k), val 
    else:  
        (mat,j,k,b_jk) = (arr[0],arr[1],int(arr[2]),arr[3]) 
        for i in range(1,N+1):
            val = [str(mat), int(j), float(b_jk)] 
            yield (i,k), val
 
# Reducer 
def reducer (key,value): 
    listA = [] 
    listB = []
    s = 0
    values = list(value) 
    for v in values: 
        if v[0] == 'A': 
            listA.append((v[1],v[2])) 
        else: 
            listB.append((v[1],v[2])) 
    for (j,a_ij) in listA: 
        for (J,b_jk) in listB: 
            if (j==J): 
                s += a_ij*b_jk
    yield key,s 

     
# Main
if __name__ == '__main__':
    bMat, n = inputToTransitionMatrix()
    oldMat, newMat = bMat, bMat
    k = 1
    maxi=1
    while maxi>=0.000001:
        dumbo.run(mapper, reducer)
        oldMat = newMat
        newMat = dictToMatrix(n)
        nextIterMatFile(newMat,bMat,n)
        k += 1
        maxi = maxValueDiff (oldMat, newMat, n)
    file = open('Results.txt','w')
    #file.write(str(diffMat))
    file.write('The Steady State matrix is \n')
    file.write(str(newMat)+'\n')
    file.write('Number of multiplications required to reach the steady state \n')
    file.write(str(k)+'\n')
    file.close()