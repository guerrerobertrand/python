'''
Created on 19 mai 2015

@author: Bertrand
'''
import fileinput
import sys

class fonctions(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''


    def replaceAll(file,searchExp,replaceExp):
        for line in fileinput.input(file, inplace=1):
            if searchExp in line:
                line = line.replace(searchExp,replaceExp)
            sys.stdout.write(line)