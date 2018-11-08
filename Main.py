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
import pickle

#SampleFiles
from libpy import Init
from libpy import TypeTrans
from libpy import GUIMain

DEBUG = 1

epision = 4;
minS = 25;
NegativeVal = 10;
Oheight = 288;
Owidth = 512;
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



def main(Model, FileLoc, FileName):
	os.system("rm -rf main")
	os.system("gcc -I ./lib main.c -o main")

	OldImg = cv2.resize(np.array(Image.open(FileLoc[0]).convert("L")), (Owidth, Oheight))
	TypeTrans.Img2Dat("df", "", "Input/Inp2.dat", OldImg)

	TrainX = []
	TrainY = []
	for kase in range(1, len(FileLoc)):
		NewImg = cv2.resize(np.array(Image.open(FileLoc[kase]).convert("L")), (Owidth, Oheight))
		
		os.system("rm -rf Input/Inp1.dat")
		os.system("mv Input/Inp2.dat Input/Inp1.dat")
		TypeTrans.Img2Dat("df", "", "Input/Inp2.dat", NewImg)
		
		os.system("./main")

		ClusImg, HogDescriptor, clusMax = ReadData()
		
		if DEBUG:
			imageio.imwrite("Output/Img1.png", OldImg)
			imageio.imwrite("Output/Img2.png", NewImg)		
		



		if Model == "train":
			Sign = GUIMain.DBSCANGUI(ClusImg, clusMax, HogDescriptor, Oheight, Owidth)

			for i in range(0, len(HogDescriptor)):
				if Sign[HogDescriptor[i][0]] == 1:
					continue

				TrainX.append(HogDescriptor[i][3:len(HogDescriptor[i])])
				if Sign[HogDescriptor[i][0]] == 2:
					TrainY.append(1)
				if Sign[HogDescriptor[i][0]] == 0:
					TrainY.append(0)




		if Model == "test":
			clf = pickle.load(open("Output/model.m", 'rb'))
			TestData = []
			for i in range(0, len(HogDescriptor)):
				TestData.append(HogDescriptor[i][3:len(HogDescriptor[i])])		
			Result = clf.predict(TestData)

			Prob = [0 for n in range(clusMax)]
			Total = [0 for n in range(clusMax)]
			for i in range(0, len(HogDescriptor)):
				Total[HogDescriptor[i][0]] += 1
				Prob[HogDescriptor[i][0]]  += Result[i]

			for i in range(0, len(Prob)):
				Prob[i] /= Total[i]
				if Prob[i] >= DetectProb:
					print("WARNING!!!!!!!!")
					break


	if Model == "train":
		clf = svm.SVC()
		clf.fit(TrainX, TrainY)

		joblib.dump(clf, "Output/model.m")

		if DEBUG:
			TestData = []
			for i in range(0, len(HogDescriptor)):
				TestData.append(HogDescriptor[i][3:len(HogDescriptor[i])])		
			Result = clf.predict(TestData)
			print(Result)
			Prob = [0 for n in range(clusMax + 1)]
			Total = [0 for n in range(clusMax + 1)]
			for i in range(0, len(HogDescriptor)):
				Total[HogDescriptor[i][0]] += 1
				Prob[HogDescriptor[i][0]]  += Result[i]

			for i in range(1, len(Prob)):
				Prob[i] /= Total[i]
				if Prob[i] >= DetectProb:
					print("WARNING!!!!!!!!")
					break
			print(Prob)
	return


if __name__ == '__main__':
	FileLoc, FileName = Init.GetSufixFile(sys.argv[2], ["png", "jpg"])
	if sys.argv[1] == "test":
		main("test", FileLoc, FileName)
	if sys.argv[1] == "train":
		main("train", FileLoc, FileName)


















