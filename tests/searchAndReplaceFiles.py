'''
Created on 19 mai 2015

@author: Bertrand
'''

import fileinput
import sys, os

if __name__ == '__main__':
    
    print("Search and Replace on multiple files")    

    # The top argument for walk
    topdir = "C:\\Users\\Bertrand\\Desktop\\stage\\"
    
    # The extension to search for
    exten = ".txt"
    
    # Loop recursively into folders
    for dirpath, dirnames, files in os.walk(topdir):
        for name in files:
            if name.lower().endswith(exten):
                print(os.path.join(dirpath, name))
                file=os.path.join(dirpath, name)
                try: 
                    print("Opening file : " + file)

                    searchExp = "\""
                    replaceExp = ""
                    for line in fileinput.input(file, inplace=True):
                        if searchExp in line:
                            line = line.replace(searchExp,replaceExp)
                        sys.stdout.write(line)
                finally:    
                    print('Done, file closed')
                    #file.close()