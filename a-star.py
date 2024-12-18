''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 20:26:15 2019

@author: Joshua L. Phillips
Department of Computer Science
Middle Tennessee State University
Illustration of heapq and operator overloading

Portions based on Python code provided by
Scott P. Morton
Center for Computational Science
Middle Tennessee State University
"""

import heapq, copy, sys


    
class PriorityQueue():
    def __init__(self):
        self.thisQueue = []
    def push(self, thisNode):
        heapq.heappush(self.thisQueue, (thisNode.val, -thisNode.id, thisNode))
    def pop(self):
        return heapq.heappop(self.thisQueue)[2]
    def isEmpty(self):
        return len(self.thisQueue) == 0
    def length(self):
        return len(self.thisQueue)

nodeid = 0
class node():
    def __init__(self, val):
        global nodeid
        self.id = nodeid
        nodeid += 1
        self.val = val
    def __str__(self):
        return 'Node: id=%d val=%d'%(self.id,self.val)


class Set():
    def __init__(self):
        self.thisSet = set()
    def add(self,entry):
        if entry is not None:
            self.thisSet.add(entry.__hash__())
    def length(self):
        return len(self.thisSet)
    def isMember(self,query):
        return query.__hash__() in self.thisSet


class state():
    def __init__(self):
        self.xpos = 0
        self.ypos = 0
        self.tiles = [[0,1,2],[3,4,5],[6,7,8]]
        self.visited = []
        self.moves = 0
    def left(self, prev):
        if (self.ypos == 0):
            return None
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos][s.ypos-1]
        s.ypos -= 1
        s.tiles[s.xpos][s.ypos] = 0
        s.visited.append(prev)
        s.moves+=1
        return s
    def right(self, prev):
        if (self.ypos == 2):
            return None
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos][s.ypos+1]
        s.ypos += 1
        s.tiles[s.xpos][s.ypos] = 0
        s.visited.append(prev)
        s.moves+=1
        return s
    def up(self, prev):
        if (self.xpos == 0):
            return None
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos-1][s.ypos]
        s.xpos -= 1
        s.tiles[s.xpos][s.ypos] = 0
        s.visited.append(prev)
        s.moves+=1
        return s
    def down(self, prev):
        if (self.xpos == 2):
            return None
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos+1][s.ypos]
        s.xpos += 1
        s.tiles[s.xpos][s.ypos] = 0
        s.visited.append(prev)
        s.moves+=1
        return s
    def __hash__(self):
        return (tuple(self.tiles[0]),tuple(self.tiles[1]),tuple(self.tiles[2]))
    def __str__(self):
        return '%d %d %d\n%d %d %d\n%d %d %d\n'%(
                self.tiles[0][0],self.tiles[0][1],self.tiles[0][2],
                self.tiles[1][0],self.tiles[1][1],self.tiles[1][2],
                self.tiles[2][0],self.tiles[2][1],self.tiles[2][2])
    def equals(self, aState):
        return self.__hash__() == aState.__hash__()
    def copy(self):
        s = copy.deepcopy(self)
        return s

            
def expand(curState, frontier, curNode, closedList, myStates, goal, h):
    #find surrounding states
    above = curState.up(curNode.id)
    below = curState.down(curNode.id)
    left = curState.left(curNode.id)
    right = curState.right(curNode.id)
    #add them to an array to go through
    children = [above, below, left, right]

    #go through array of children
    for child in children:
        #add the child if it is not empty or on the closed list
        if child is not None and not closedList.isMember(child):
            myStates.append(child)
            frontier.push(node(child.moves + heu_cost(child, goal, h)))
    #return updated frontier and states
    return myStates, frontier
def heu_cost(childNode, goal, h):
    #if hueristic is 0, return 0
    if h == 0:
        return 0
    #if h = 1, then add the amount of tiles that are not aligned w the goal
    elif h == 1:
        displaced = 0
        for i in range(3):
            for j in range(3):
                if childNode.tiles[i][j] != goal.tiles[i][j]:
                    displaced += 1
        return displaced
    #if h == 2, then do manhattan distancce
    elif h == 2:
        total_distance = 0
        current_tiles = childNode.tiles
        goal_x = 0
        goal_y = 0
    
        for x in range(3):
            for y in range(3):
                if current_tiles[x][y] != 0:  # Skip the blank tile (0)
                    #go through goal tiles
                    for i in range(3):
                        for j in range(3):
                            if goal.tiles[i][j] == current_tiles[x][y]:
                                #if they match, save the goals x and y
                                goal_x = i
                                goal_y = j
                    #calculate
                    total_distance += abs(x - goal_x) + abs(y - goal_y)
        return total_distance
    #max heuristic
    elif h == 3:
        current_tiles = childNode.tiles
        max_h = 0
        goal_x = 0
        goal_y = 0
        for x in range(3):
            for y in range(3):
                if current_tiles[x][y] != 0:  # Ignore the empty tile
                    # Calculate the goal position
                    for i in range(3):
                        for j in range(3):
                            if goal.tiles[i][j] == current_tiles[x][y]:
                                #if they match, save the goals x and y
                                goal_x = i
                                goal_y = j
                    max_h = max(max_h, abs(x - goal_x) + abs(y - goal_y))
    
        return max_h
    

def printFunc(V, N, d, b, curState, myStates):
    print("V = ", V)
    print("N = ", N)
    print("d = ", d)
    print("b = ", b)
    #for each visited state
    for i in range(len(curState.visited)):
        #print the state from the begining
        print(myStates[curState.visited[i]].__str__()) 
    #print the current one
    print(curState.__str__())
def main():
    
    frontier = PriorityQueue()
    closedList = Set()
    myStates = []
    heu_choice = int(sys.argv[1])

    #temporary list
    curInputs = []
    

    #goal board
    goal = state()
    goal.tiles = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

    #board from random
    for line in sys.stdin:
        curInputs += line.split()
    
    board = [[int(curInputs[0]), int(curInputs[1]), int(curInputs[2])], [int(curInputs[3]), int(curInputs[4]), int(curInputs[5])], [int(curInputs[6]), int(curInputs[7]), int(curInputs[8])]]


    #find position of 0
    for x in range(3):
        for y in range(3):
            if board[x][y] == 0:
                xPos, Ypos = x, y
                break
            
    #create the board start state
    start = state()
    start.tiles = board
    start.xpos = xPos
    start. ypos = Ypos
    #add to myStates array
    myStates.append(start)
    #push it to the frontier
    frontier.push(node(heu_cost(start, goal, heu_choice)))

    V = 0
    N = 0
    d = 0
    b = 0

    while not frontier.isEmpty():
        #pop the least costing state
        curNode = frontier.pop()
        curState = myStates[curNode.id]
        #add it to the closed list
        closedList.add(curState)
        V += 1

        #if we reached the goal state
        if curState.equals(goal):
            d = curState.moves
            N = len(myStates) + closedList.length()
            if curState.moves != 0:
                b = (N) ** (1/d)
            else:
                b = 0
            printFunc(V, N, d, b, curState, myStates)
            break
            #if we haven't expand the children
        myStates, frontier = expand(curState, frontier, curNode, closedList, myStates, goal, heu_choice)



    
main()
