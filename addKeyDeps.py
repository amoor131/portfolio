# Anthony Moore
# amoor131
# sorted alphabet
# 1/22/21
#
# What it does:
# Organize4 works, but my goal here is to make this work faster than that.
# organized4 is terribly slow so this will hopefully cut the time down substantially
#
# Possible improvements:
# order letters in words by least to most frequent to reduce comparisons
# 

#from curses.ascii import isalpha
#from sys import argv

#dictionary that will hold keys and words made with them
engDict = {}

#used to see if key already exists
def isKey(testKey):
    if testKey in engDict.keys():
        return True
    else:
        return False
        
#not yet implemented!
#meant to sort each word by letter frequency
#not sure if the time saved in comparisons is greater than the time spent sorting very word
#def freqOrder(word):
    # according to https://www3.nd.edu/~busiforc/handouts/cryptography/letterfrequencies.html
    # this is the order of least to most frequent letters as they appear in the english language.
    # this will be used to reduce the number of comparisons
    #frequency = ['Q','J','Z','X','V','K','W','Y','F','B','G','H','M','P','D','U','C','L','S','N','T','O','I','R','A','E']

#returns true is all letters in testWord are in keyWord
def fitsIn(testWord, keyWord):
    comp = list(keyWord)
    if len(testWord) <= len(keyWord):
        for letter in testWord.strip('\n'):
            #print(f"letter: {letter}| keyWord: {keyWord}") #DEBUG
            if letter in comp:
                comp[comp.index(letter)] = '#'
            else:
                return False
        #only returns true if all letters were found in keyWord
        return True

import json
'''
def addKey(testKey):
    #used to add new lines to f statements
    new_line = '\n'
    #check that the entry is only letters
    if isalpha(testKey) == False:
        return -1
    #double check that the user input isn't already a key in the database
    if isKey(testKey):
        return -2
    #user input in reverse alphabetical order, 
    sortedKey = ''.join(sorted(testKey.strip('\n')))
    foundWords = ''
    with open('sorted_length.txt','r') as engWords:
        for word in engWords:
            if fitsIn(word, testKey):
                foundWords += ' ' + ''.join(word.strip('\n')) # not sure if I need to strip new line
        if len(foundWords) > 0:
'''            
    #print("===============end===============")