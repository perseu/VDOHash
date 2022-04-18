# -*- coding: utf-8 -*-
"""
This script is meant to validate video. First we need to create a hash file from the video that we want to protect.
Afterward that hash file must be stored so that it can be used in the future to validate any file that is said to be the file that we are 
protecting. If there is even on bit changed, this script will detect in which frame that change was made.
This works with any file that OpenCV can open.

Created on Fri Apr  18 14:38:32 2022

@author: Joao Aguas
"""
import os
import sys
import cv2
import time
from hashlib import sha256



class blockchain:
    def __init__(self):
        self.fnum = 0
        self.yourmark = 'There is a fucking war on. The Russians are invading Ukrain.' # A string about the state of the world.
        self.nseed = 0    # It's a int that will be converted into a string.
        self.hsh = 0
        self.lasthsh = 0
        self.genblock = []
        self.thechain = []
        
    def initBlChain(self):
        self.hsh = sha256(sha256(str(self.nseed).encode('utf-8')).hexdigest().encode('utf-8') + sha256(self.yourmark.encode('utf-8')).hexdigest().encode('utf-8'))
        self.genblock = [self.fnum, self.nseed, self.hsh.hexdigest()]
        self.lasthsh = self.hsh
        self.thechain.append(self.genblock)
    
    def frameHash(self, frame):
        self.fnum += 1
        self.hsh = sha256(self.lasthsh.hexdigest().encode('utf-8') + sha256(frame.ravel()).hexdigest().encode('utf-8'))
        self.lasthsh = self.hsh
        self.thechain.append([self.fnum, self.nseed, self.hsh.hexdigest()])
        
    def dumpChain(self):
        return self.thechain


class videoControl:
    def __init__(self):
        self.vidLoc = '-0000'
        
    def setVidLoc(self, vidpath): 
        if os.path.isfile(vidpath):
            if os.path.getsize(vidpath) > 0:
                self.vidLoc = vidpath
            else:
                self.vidLoc = '-1111' # Means file empty
        else:
            self.vidLoc = '-9999' # Means file not found.
        
    def downloadVid(self):
        if self.vidLoc == '-1111':
            print('\nERROR: File is empty!!! Seems that there is nothing but VOID in there.\n')
        elif self.vidLoc == '-9999':
            print('\nERROR: The file was not where. Maybe it took the wrong BUS?!\n')
        elif self.vidLoc == '-0000':
            print('\nERROR: Lacking the path to the file. If you wanna go somewhere, you\'ve to tell me!!!')
        else:
            cap = cv2.VideoCapture(self.vidLoc)
            return cap
        

        
        
if __name__ == '__main__':
    
    start = time.time()
    filepath = []  
    outputfile = [] 
    opt = 0
    invalid = 0
    
    # r - reference video. Or video that creates the list hash values.
    # t - video to be validated. It's the video that we're attempting to see if it is the same as the reference.
    # o - Hash output file.
    # i - Input hash reference file.
    # h - Help
    args = sys.argv
    
#    args = ['batch.py','t=testvideo.MP4', 'i=test_output.txt']
    
    for argument in args:
        argtemp = argument.split('=')
        if argtemp[0] == 'r':
            filepath = argtemp[1]
            opt += 1
        if argtemp[0] == 't':
            filepath = argtemp[1]
            opt -= 1
        if argtemp[0] == 'o':
            outputfile = argtemp[1]
            opt += 1
        if argtemp[0] == 'i':
            outputfile = argtemp[1]
            opt -= 1        
        if argtemp[0] == 'h' or len(args) == 1:
            print("\n\nTo create the list of hash of the reference video and create a output file with the list of hash.")
            print(args[0] + " r=ReferenceVideoPath o=outputHashFile\n")
            print("To validate a video using a text file with the hash list.")
            print(args[0] + " t=PathToVideoToValidate i=hashfile\n")
            exit()
    
    vid = videoControl()
    blkconst = blockchain()
    
    blkconst.initBlChain()
    
    vid.setVidLoc(filepath)
    cap = vid.downloadVid()
    
    while(cap.isOpened()):
        ret, frame = cap.read()
        if frame is not None:
            blkconst.frameHash(frame)
        else:
            print('\nFrame is empty')
        
        if not(ret):
            print('\nDumping chain!\n')
            chainres = blkconst.dumpChain()
            break
        
    cap.release()

    if opt == 2:
        print('\nWriting the output file...\n')    
        outfile = open(outputfile,'w')
        for element in chainres:
            outfile.write(str(element[0]) + ' ' + str(element[1]) + ' ' + str(element[2]) + '\n')
            
        outfile.close()
        
    elif opt == -2:
        hashlist = []
        infile = open(outputfile,'r')
        refhashes = infile.readlines()
        if len(chainres) != len(refhashes):
            print('\n\nThe number of frames should be ' + len(chainres) + ' and it\'s ' + len(refhashes) + '\nThis is not the same video file.')
            exit()
        else:
            for ii in range(len(chainres)):
                if chainres[ii][2] != (refhashes[ii]).split()[2]:
                    invalid = ii
            if invalid > 0:
                print('\n\nALERT: Video check failed in frame '+ invalid + '\n')
            else:
                print('\n\nVideo file is verified!!!\n\n')
                
    else:
        print('\n\nINVALID PARAMETERS!!!')
        print("\n\nTo create the list of hash of the reference video and create a output file with the list of hash.")
        print(args[0] + " r=ReferenceVideoPath o=outputHashFile\n")
        print("To validate a video using a text file with the hash list.")
        print(args[0] + " t=PathToVideoToValidate i=hashfile\n")
    
    end = time.time()    
    print('\nIt took ',end-start,'seconds to finish.')