'''
Created on Oct 12, 2016

@author: kwdalle
Author: Kevin Dalle
Copyright: 10/12/16
'''
import sys
import re

valStack = [] #Used for computing the value of the string if it is valid

def state0(inputStack, stack):
    i = inputStack.pop()
    stack.append(i) #Pushes the token onto the stack
    if (isAnumber(i)):
        stack.append(5) #Pushes the state onto the stack
        printStack(inputStack, stack)
        state5(inputStack, stack)
    elif i == "(":
        stack.append(4) #Same as above
        printStack(inputStack, stack)
        state4(inputStack, stack) 
    else:
        invalid()
        
def state1(inputStack, stack):
    i = inputStack.pop()
    if (i == "+" or i == "-"): #Implements the rules for shifting to 6 from this state
        stack.append(i)
        stack.append(6)
        printStack(inputStack, stack)
        state6(inputStack, stack)
    elif(i == "$"): #For when it is time to accept the string as valid.
        print"Valid------->" + str(valStack.pop()) #Also prints out the calculated value of the input
        sys.exit()
    else:
        invalid()
        
def state2(inputStack, stack):
    i = inputStack.pop()
    cstate = stack.pop() #Pops off the current state
    token = stack.pop() #Pops off the token to the above state
    prevState = stack.pop() #Pops off to get the previous state and then pushes it back 
    stack.append(prevState) #to the stack
    if (i == "+" or i == "-" or i == ")" or i == "$"): #Beginning of the reduction rule
        inputStack.append(i)
        #Fails if the token is not T since it matches no reduction
        if (token == "T"):
            stack.append("E")
        else:
            invalid()
        #If determines where to go based on the previous state if its neither of those it fails
        if prevState == 0:
            stack.append(1)
            printStack(inputStack, stack)
            state1(inputStack, stack)
        elif prevState == 4:
            stack.append(8)
            printStack(inputStack, stack)
            state8(inputStack, stack)
        else:
            invalid()
    elif(i == "*" or i == "/"): #Deals with the shifting part of the state and puts the data back on the stack since it was not reduced
        stack.append(token)
        stack.append(cstate)
        stack.append(i)
        stack.append(7)
        printStack(inputStack, stack)
        state7(inputStack, stack)
    else:
        invalid()

def state3(inputStack, stack):
    i = inputStack.pop()
    token = stack.pop()
    token = stack.pop()
    prevState = stack.pop()
    stack.append(prevState)
    #Deals with all the reduction rules.
    if (i == "+" or i == "-" or i == "*" or i == "/"
    or i == ")" or i == "$"):
        inputStack.append(i)
        if(token == "F"):
            stack.append("T")
            if prevState == 0 or prevState == 4:
                stack.append(2)
                printStack(inputStack, stack)
                state2(inputStack, stack)
            elif prevState == 6:
                stack.append(9)
                printStack(inputStack, stack)
                state9(inputStack, stack)
            else:
                invalid()
        else:
            invalid()
    else:
        invalid()
        
def state4(inputStack, stack):
    #Call's the state0 function since they use the same rules.
    state0(inputStack, stack)
    
def state5(inputStack, stack):
    i = inputStack.pop()
    token = stack.pop()
    token = stack.pop()
    prevState = stack.pop()
    stack.append(prevState)
    #Also deals with all reduction rules
    if (i == "+" or i == "-" or i == "*" or i == "/"
    or i == ")" or i == "$"):
        inputStack.append(i)
        if(isAnumber(token)):
            valStack.append(float(token)) #Puts the value on the stack to be computed later
            stack.append("F")
            if prevState == 0 or prevState == 4 or prevState == 6:
                stack.append(3)
                printStack(inputStack, stack)
                state3(inputStack, stack)
            elif prevState == 7:
                stack.append(10)
                printStack(inputStack, stack)
                state10(inputStack,stack)
            else:
                print prevState
                invalid()
        else:
            invalid()
    else:
        invalid()
        
def state6(inputStack, stack):
    state0(inputStack, stack)
    
def state7(inputStack, stack):
    state0(inputStack, stack)
    
def state8(inputStack, stack):
    i = inputStack.pop()
    stack.append(i) #Pushes the token onto the stack
    if (i == "+" or i == "-"):
        stack.append(6) #Pushes the state onto the stack
        printStack(inputStack, stack)
        state6(inputStack, stack)
    elif i == ")":
        stack.append(11) #Same as above
        printStack(inputStack, stack)
        state11(inputStack, stack) 
    else:
        invalid()
        
def state9(inputStack, stack):
    i = inputStack.pop()
    if(i == "+" or i == "-" or i == ")" or i == "$"): #Deals with the reduction rules
        inputStack.append(i)
        T = stack.pop()
        T = stack.pop()
        operator = stack.pop()
        operator = stack.pop()
        E = stack.pop()
        E = stack.pop()
        prevState = stack.pop()
        stack.append(prevState)
        updateValStack(operator)
        if(operator == "+" and E == "E" and T == "T"):
            stack.append("E")
            if prevState == 0:
                stack.append(1)
                printStack(inputStack, stack)
                state1(inputStack, stack)
            elif prevState == 4:
                stack.append(8)
                printStack(inputStack, stack)
                state8(inputStack, stack)
            else:
                print prevState
                invalid()
        elif(operator == "-" and E == "E" and T == "T"):
            stack.append("E")
            if prevState == 0:
                stack.append(1)
                printStack(inputStack, stack)
                state1(inputStack, stack)
            elif prevState == 4:
                stack.append(8)
                printStack(inputStack, stack)
                state8(inputStack, stack)
            else:
                print prevState
                invalid()
        else:
            invalid()
    elif(i == "*" or i == "/"): #Deals with the shifting, data was only popped off if a reduction rule was in effect, so no need to put it back on the stack
        stack.append(i)
        stack.append(7)
        printStack(inputStack, stack)
        state7(inputStack, stack)
    else:
        invalid()
        
def state10(inputStack, stack):
    i = inputStack.pop()
    inputStack.append(i)
    if(i == "+" or i == "-"or i == "*" or i == "/" or i == ")" or i == "$"): #Deals with the reduction rules. No shifting in this state
        F = stack.pop()
        F = stack.pop()
        operator = stack.pop()
        operator = stack.pop()
        T = stack.pop()
        T = stack.pop()
        prevState = stack.pop()
        stack.append(prevState)
        updateValStack(operator)
        if(operator == "*" and T == "T" and F == "F"):
            stack.append("T")
            if prevState == 0 or prevState == 4:
                stack.append(2)
                printStack(inputStack, stack)
                state2(inputStack, stack)
            elif prevState == 6:
                stack.append(9)
                printStack(inputStack, stack)
                state9(inputStack, stack)
            else:
                print prevState
                invalid()
        elif(operator == "/" and T == "T" and F == "F"):
            stack.append("T")
            if prevState == 0 or prevState == 4:
                stack.append(2)
                printStack(inputStack, stack)
                state2(inputStack, stack)
            elif prevState == 6:
                stack.append(9)
                print stack
                printStack(inputStack, stack)
                state9(inputStack, stack)
            else:
                print prevState
                invalid()
        else:
            invalid()
    else:
        invalid()
            
def state11(inputStack, stack):
    i = inputStack.pop()
    inputStack.append(i)
    if (i == "+" or i == "-" or i == "*" or i == "/" or i == ")" or i == "$"): #Deals with the reduction rules. No shifting in this state
        p1 = stack.pop()
        p1 = stack.pop()
        E = stack.pop()
        E = stack.pop()
        p2 = stack.pop()
        p2 = stack.pop()
        prevState = stack.pop()
        stack.append(prevState)
        if (p1 == ")" and E == "E" and p2 == "("):
            stack.append("F")
            if prevState == 7:
                stack.append(10)
                printStack(inputStack, stack)
                state10(inputStack, stack)
            elif prevState == 6 or prevState == 4 or prevState == 0:
                stack.append(3)
                printStack(inputStack, stack)
                state3(inputStack, stack)
            else:
                invalid()
        else:
            invalid()
    else:
        invalid()
        
def printStack(inputStack, stack):
    #Printing the stack in the the chosen format
    x = 0
    while x < len(stack):
        print "["+str(stack[x])+":"+str(stack[x+1])+"]",
        x += 2
    print "   ", 
    x = len(inputStack) - 1
    while x > -1:
        print inputStack[x],
        x-=1
    print""

def invalid():
    print "Invalid"
    sys.exit()
    
def isAnumber(n):
    try:
        float(n)
        return True
    except ValueError:
        return False
    
def updateValStack(operator):
    val1 = valStack.pop()
    val2 = valStack.pop()
    if(operator == "+"):
        valStack.append(val2 + val1)
    elif(operator == "-"):
        valStack.append(val2-val1)
    elif(operator == "*"):
        valStack.append(val2*val1)
    elif(operator == "/"):
        valStack.append(val2/val1)
        
if __name__ == '__main__':
    arguments = sys.argv
    print arguments[1] + "$" #Printing the string for testing purposes
    stack =  re.findall('[+-/*()]|\d+',arguments[1]) #Splits the string while keeping the delimiters
    stack.append("$")
    stack.reverse() #Reverses the stack to get it in the correct order
    tokenStack = ["-",0]
    state0(stack,tokenStack)
