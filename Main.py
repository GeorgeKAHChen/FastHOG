#===============================================================
#
#		FastHog project
#		TmpMain.py	
#		Copyright by KazukiAmakawa, all right reserved
#
#===============================================================

#Normal
import os
import sys
import os.path
from collections import deque
from copy import deepcopy

#Science Calculation
import math
import matplotlib.patches as patches
import numpy as np
import matplotlib.pyplot as plt

#Image Processing
import imageio
from PIL import Image
from PIL import ImageFilter
import cv2 

#Algorithms
import datetime
from sklearn.externals import joblib
from sklearn import svm

#SampleFiles
from libpy import Init
from libpy import TypeTrans
from libpy import GUIMain

DEBUG = 1

epision = 4;
minS = 25;
NegativeVal = 10;
Oheight = 144;
Owidth = 256;
height = 32;
width = 18;
DetectProb = 0.5;



def ReadData():
	ClusImg = np.array(TypeTrans.Dat2Img("fd", "Output/ClusterImg.dat", "", []))
	HogDescriptor = []
	clusMax = 0

	FileName = "Output/HogDEMOResult.dat"
	File = open(FileName, "r")
	while 1:
		FileLine = File.readline()
		if not FileLine:
			break
		HogDescriptor.append(FileLine.strip().split(' '))

	for i in range(0, len(HogDescriptor)):
		for j in range(0, len(HogDescriptor[i])):
			if j == 0 or j == 1 or j == 2:
				HogDescriptor[i][j] = int(HogDescriptor[i][j])
				if j == 0:
					clusMax = max(clusMax, HogDescriptor[i][0])
			else:
				HogDescriptor[i][j] = float(HogDescriptor[i][j])

	return ClusImg, HogDescriptor, clusMax



def GUISign():
	return

def SVMTrain():
	return 

def Detection():
	return

def main(Model, FileLoc, FileName):
	os.system("rm -rf main")
	os.system("gcc -I ./lib main.c -o main")

	OldImg = cv2.resize(np.array(Image.open(FileLoc[0]).convert("L")), (Owidth, Oheight))
	TypeTrans.Img2Dat("df", "", "Input/Inp2.dat", OldImg)
	for kase in range(1, len(FileLoc)):
		NewImg = cv2.resize(np.array(Image.open(FileLoc[kase]).convert("L")), (Owidth, Oheight))
		
		os.system("rm -rf Input/Inp1.dat")
		os.system("mv Input/Inp2.dat Input/Inp1.dat")
		TypeTrans.Img2Dat("df", "", "Input/Inp2.dat", NewImg)
		
		os.system("./main")

		ClusImg, HogDescriptor, clusMax = ReadData()
		
		print(clusMax)

		if DEBUG:
			imageio.imwrite("Output/Img1.png", OldImg)
			imageio.imwrite("Output/Img2.png", NewImg)
			imageio.imwrite("Output/ClusImg.png", ClusImg)

		
		if Model == "train":
			print("Sorry, not finished")
			#sign with GUI
			#train SVM
			#save model

		if Model == "test":
			print("Sorry, not finished")
			#read model
			#predict
			#probability decision
			#return result


	return


if __name__ == '__main__':
	FileLoc, FileName = Init.GetSufixFile(sys.argv[2], ["png", "jpg"])
	if sys.argv[1] == "test":
		main("test", FileLoc, FileName)
	if sys.argv[1] == "train":
		main("train", FileLoc, FileName)


















