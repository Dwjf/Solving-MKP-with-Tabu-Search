import random
import matplotlib.pyplot as plt

def engine(n,list1):
    
    def listoflist(original_list,variable):
        "converts list of int to list of lists.Test"
        start=0
        list1=[]
        for i in range(int(len(original_list)/variable)):
            list1.append(original_list[start:start+variable])
            start = start + variable
        return list1

    def listopen(list1):
        """
        input:list
        returns tuple of 2 int and 3 lists
        ######
        Parameter 'list1' = a list of single int passed from loader()

        Purpose: The purpose of this function to 'divide' the components of
        list1 into the respective sections, for further processing.The sections
        are variable, constraint, optimal value(0 if none), list of coefficients,
        list of constraints, and list of Right Hand Side(RHS) values.

        listoflist() is to convert a list into a list of lists. Constraints
        in its proper form is a list of constraint coefficients , by number of 
        constraints.
        """  
        variable=list1[0]
        constraint=list1[1]
        optimal = list1[2]
        initial=3
        list_coefficient=list1[initial:initial+variable]
        list_constraint = list1[initial+variable:-constraint]
        newlist=listoflist(list_constraint,variable)
        list_rhs=list1[-constraint:len(list1)]

        return variable ,list_coefficient,newlist,list_rhs,optimal
    



    '''
    def constraintlist(r):
        """
        returns list of list
        This was important, because it helped me to learn how
        to make a list of lists from a list. Basically every iteration
        started a new list.
        
        """
        list3=[]
        for i in r:
            a=tolist(i)
            list3.append(a)
        return list3
    '''

    def fitness(listgene):
        """
        returns int
        -----------------------------------
        Parameter 'listgene' = List of binaries(0,1)

        Purpose: This returns an int representing the fitness of a 
                binary solution
        
        Variable 'coeff' is a variable passed from listopen()

        """
        valuelist=[]
        for i in range(len(listgene)):
            score=coeff[i]*listgene[i]
            valuelist.append(score)
        v=sum(valuelist)
        return v

    def isfeasible_constraint(constraint,rhs,genes):
        """
        returns True
        ___________________________________________

        Parameter 'constraint' = list of constraints
        Parameter ' rhs' = list of RHS values
        Parameter 'genes' = list of int values, representing binary
        All these parameters are returned from listopen()
        
        Purpose: Returns true when all constraints are satisfied i.e

        LHS one constraint <= RHS

        """
        list2=[]
        for i in range(len(constraint)): # boolean check for single list
            s1=constraint[i]*genes[i]
            list2.append(s1)
        
        if sum(list2)<=rhs:
            return True
        else:
            return False

    def isfeasible_mult_constraints(constraints,list1):
        """
        returns Boolean

        Parameter 'constraints' from fileopen()
        Parameter 'list1' = 1 list of gene values
        """
        for j in range(len(constraints)): # selects a list from lists
            if isfeasible_constraint(constraints[j],rhs[j],list1):
                continue
            else:
                return False
        return True


    def indexpositions(list1,int1):
        """
        to return positions of int in list

        Parameter 'list1' would be list of int
        Parameter 'int1' would be either '0' or '1'

        """
        list2=[]
        for i in range(len(list1)):
            if int1==list1[i]:
                list2.append(i)
        return list2

    def istabu(list1,int1):
        """ 
        returns Boolean
        ----------------------------------------
        Parameter 'list1' is tabu list
        Parameter 'int' is index ,which refers to the index of the tabu ist
        """
        if list1[int1]>0:
            return True

    def move(list1,tt):
        """
        return one tuple (list,int,int)
        
        -----------------------------------------
        Parameter 'list1' would be the candidate gene list

        Purpose: This generates a move candidate, with the 
        index of the add,drop tabu move. If this candidate is
        selected, the add/drop tabu move will update the tabu list
        
        """
        list3=[]
        finallist=[]
        list3,droptabu=add(list1,tt)
        finallist,addtabu=drop(list3,droptabu,tt)
        return finallist,droptabu,addtabu


    def updatetabu(tuple1,tt,variable):
        """
        input:solution tuple
        updates tt list
        --------------------------------------
        Parameter 'tuple1' = tuple of the best candidate, with drop/add tabu moves

        Variable tt, representing tabu list, is declared at line 315

        """
        #global tt
        #droptenure = int(variable/25)
        #addtenure = int(variable/50)
        droptenure = 15
        addtenure = 15
        tt[tuple1[0][1]]=droptenure
        tt[tuple1[0][2]]=addtenure
        #return finallist,droptabu,addtabu



    def flip(index,list1):
        """
        flip a binary value
            returns list
        
        Parameter 'index' is an integer given by 'pick' variable in the
        add() or drop() function.

        """
        list2=list1[:] #clones a list
        if list2[index]==0:
            list2[index]=1
        else:
            list2[index]=0
        return list2


    def add(list1,tt):
        """
        returns tuple, of a list, and str
        -----------------------------------
        Parameter 'list1' = candidate list 
        
        """
        list2=[] #list to store "0" indexes
        list3=[] #new return list
        list2=indexpositions(list1,0)#list of "0" indexes
        pick=random.choice(list2) #pick a initialchoice of the index no."Pick" is int
        while istabu(tt,pick): #while pick is tabu,repeat till valid pick is found
            pick=random.choice(list2)
        list3=flip(pick,list1)
        return list3,pick

    def drop(list1,addpick,tt):
        """returns a list, and tabu list index"""
        list2=[] #list to store "0" indexes
        list3=[] #new return list
        list2=indexpositions(list1,1)#list of "1" indexes
        pick=random.choice(list2) #pick a initialchoice of the index no."Pick" is int
        while istabu(tt,pick) or pick==addpick: #while pick is tabu,repeat till valid pick is found
            pick=random.choice(list2)
        list3=flip(pick,list1)
        return list3,pick

    def reducetabu(tt):
        """
        updates tabu list
        
        Parameter 'tt' is a list
        """
        #global tt
        for i in range(len(tt)):
            if tt[i]!=0:
                tt[i]=tt[i]-1

    def candidatelist(list1,tt):
        """
        returns list of tuples
        
        Parameter 'list1' is the starting gene to generate multiple candidates lists

        move() generates tuple ,where first value of tuple is gene, and next tuple
        the add, drop tabu positions.

        Number of candidates are the length of the gene.
        
        """
        list2=[]
        if isinstance(list1, tuple):
            for i in range(len(list1[0])):
                list2.append(move(list1[0][0],tt))
        else:
            for i in range(len(list1)):
                list2.append(move(list1,tt))
        return list2


    def bestcandidate(list1):
        """
        input:list of tuples
        evaluates list of tuples and 
        returns: tuple

        """ 

        besttuple=()
        besttuplefitness=0
        for t in list1:
            """
            if len(t)==2:
                f=fitness(t[0][0])
            else:
                f=fitness(t[0])
            """
            f=fitness(t[0])
            if f>besttuplefitness and isfeasible_mult_constraints(constraints,t[0]):
                besttuple=t
                besttuplefitness=f
        return besttuple,besttuplefitness

    def initialise(variable):#x in length of variable
        """input:int
            returns: list

        
        Parameter 'variable' is an int, which represent the number of x values.

        Tabu list, tt, is cloned from initial list,which is a list of zeros.

        """
        initial=[]
        
        for i in range(variable):
            initial.append(0)
        tt=initial[:]
        #create list of zeros of length x
        for j in range(len(initial)):
            initial[j]=1
            if isfeasible_mult_constraints(constraints,initial):
                continue
            else:
                initial[j]=0 #reset back to zero
                initialfitness = fitness(initial)
                return initial,tt,initialfitness
            

    def main(iterations):
        """
        Parameter 'iterations' is the number of times improvement is run

        """
        #global tt #values of tt updated in function updates global
        s=initialise(variable)

        seed,tt,initialfitness =s[0],s[1],s[2]
        bestfitness=0
        best=()
        bestlist=[]
        iterationlist=[]
        for k in range(iterations):
            #reducetabu(tt) #each iteration reduce tabu tenure
            list1=candidatelist(seed,tt) # generate candidates
            reducetabu(tt)
            temp=bestcandidate(list1)
            if temp[1]!=0: # to guard against 0 value
                solution=temp
            if solution[1]>bestfitness:
                bestfitness=solution[1]#assign best int value
                best=solution[:]#clone the list binary solution to best list
            seed=solution[0][0]# clone binary to seed for next iteration
            updatetabu(solution,tt,variable)# update tabu moves
            bestlist.append(solution[1])#this is used to plot iteration axis in graph
            iterationlist.append(k)#this is used to plot iteration axis in graph
            #print("S",solution)
            #print("B","k",k,best,)
            f=fitness(solution[0][0])
        y,x=bestlist,iterationlist   
        plt.plot(x,y) #uncomment to show graph
        #plt.plot(best[1],k)
        plt.show() #uncomment to show graph
        return best,y,x,initialfitness


    #########INITIALISATION#############
    #this statement to convert tuple return values from listopen()
    #to variables in engine()
    variable,coeff,constraints,rhs,optimal=listopen(list1)

    #initialise tabu list, tt
    #tt = initialise(variable)[1]

    #return values from main()
    e=main(n)
    #return tt
    return e[3],e[0][1],e[0][0][0]


