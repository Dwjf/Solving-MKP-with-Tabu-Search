
def loader():

    def readlist():
        """ 
        returns :list of int
        tolist parses the list to proper integers
        Reads text file and returns a list 
        
        """
        f=open("/Volumes/WINDATA/Thesis/dissertation1/data/mknapcb7.txt")
        string1=(f.read())
        list1=tolist(string1)

        return list1

    def readsets(list1):
        '''
        returns list of lists

        start from 1 , because position 0 is the set number.
        size() is to determine the size of 1 set
        This loop will size up each sets according to its number of int
        determined by size() into a list of lists
        v=variable in text file
        c = contraint in text file
        '''
        start=1
        list2=[]
        for i in  range(30):
            v=list1[start]
            c=list1[start+1]
            z=size(v,c)
            list2.append(list1[start:start+z])
            start = start+z
        return list2


    def size(v,c):
        "determine size of 1 set"
        setsize=3+v+(v*c)+c
        return setsize
    
    def tolist(string):
        """
        returns list
        Parse string to two levels. First to remove space, then \n
        """
        string0=string.strip()
        string1 = string0.rstrip('\n')
        list1=string1.split(" ") # this converts the line number text to a list
        
        list2=[]
        for x in list1:# this removes blanks and puts into new list
            if x !="":
                if x!='\n':
                    list2.append(int(x))
        return list2

    ll=readsets(readlist())
    return ll # the main output of this nested function

####RUN####################################################################
import random
import matplotlib.pyplot as plt
#from setsnested import loader
from tabunested import engine

l2=loader()#returns list of list
counter=0
for i in l2:#i is for one list
    a,b=(counter,engine(500,i))
    print(a,b)
    #print(counter,engine(500,i))
    f= open("solution.txt","a+")
    f.write("%d,%d,%s\r\n" % (b[0],b[1],b[2]))
    f.close() 
    counter=counter+1