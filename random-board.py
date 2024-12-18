#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 20:26:15 2019

@author: Joshua L. Phillips
Department of Computer Science
Middle Tennessee State University
Illustration of random movement generation

Portions based on Python code provided by
Scott P. Morton
Center for Computational Science
Middle Tennessee State University
"""

import sys, numpy.random as random


# There is no error checking in this code
# Well formatted input is assumed as well as
# proper processing given well-formed input

def main():
    goalInputs = []
    for line in sys.stdin:
        goalInputs += line.split()
    
    goal = [[int(goalInputs[0]), int(goalInputs[1]), int(goalInputs[2])], [int(goalInputs[3]), int(goalInputs[4]), int(goalInputs[5])], [int(goalInputs[6]), int(goalInputs[7]), int(goalInputs[8])]]
    
    # Just once
    rng = random.default_rng(int(sys.argv[1]))
    number_of_moves = int(sys.argv[2])
    board = goal
    blankRow = 0
    blankCol = 0
    
    # Can call this as many times as needed to generate moves...
    for x in range(number_of_moves):
        # These moves will be 0,1,2,3 which can each be
        # associated with a particular movement direction
        # (i.e. up, down, left, right).
        move = rng.integers(4) 

        if move == 0:
            #move up
            if blankRow > 0: #makes sure its not already on the first row
                temp = board[blankRow-1][blankCol]     #saves the value on the row above
                board[blankRow-1][blankCol] = 0        #sets the row above to 0
                board[blankRow][blankCol] = temp       #switches value with one below
                blankRow -= 1                          #updates the row
                
            
        elif move == 1:
            #move down
            if blankRow < 2:
                temp = board[blankRow+1][blankCol]     #saves the value on the row below
                board[blankRow+1][blankCol] = 0        #sets the row below to 0
                board[blankRow][blankCol] = temp       #switches value with one above
                blankRow += 1                          #updates the row
            
        elif move == 2:
            #move left
            if blankCol > 0:
                temp = board[blankRow][blankCol-1]     #saves value on the left
                board[blankRow][blankCol-1] = 0        #sets the left to 0
                board[blankRow][blankCol] = temp       #switches value with left
                blankCol -= 1                          #updates the column
            
        elif move == 3:
            #move right
            if blankCol < 2:
                temp = board[blankRow][blankCol+1]     #saves the value on the row below
                board[blankRow][blankCol+1] = 0        #sets the row below to 0
                board[blankRow][blankCol] = temp       #switches value with one below
                blankCol += 1                          #updates the row


    output = open("output.txt", "w")
    for row in board:
        rowstr = " ".join(map(str, row))
        sys.stdout.write(rowstr)
        output.write(rowstr + '\n')
        print()
    output.close()
main()
