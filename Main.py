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
from sklearn.svm import LinearSVC
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
	HogDescriptor = [[0]]

	FileName = "Output/HogDEMOResult.dat"
	File = open(FileName, "r")
	while 1:
		FileLine = File.readline()
		if not FileLine:
			break
		HogDescriptor.append(FileLine.strip().split(' '))

	File.close()
	for i in range(0, len(HogDescriptor)):
		for j in range(0, len(HogDescriptor[i])):
			if HogDescriptor[i][j] == "nan":
				HogDescriptor[i][j] = 0.0
			else:
				HogDescriptor[i][j] = float(HogDescriptor[i][j])
	

	clusMax = len(HogDescriptor) - 1
	return ClusImg, np.array(HogDescriptor), clusMax



def main(Model, FileLoc, FileName):
	os.system("rm -rf mainpy")
	os.system("gcc -I ./lib mainpy.c -o mainpy")

	OldImg = cv2.resize(np.array(Image.open(FileLoc[0]).convert("L")), (Owidth, Oheight))
	TypeTrans.Img2Dat("df", "", "Input/Inp2.dat", OldImg)

	TrainX = []
	TrainY = []
	for kase in range(1, len(FileLoc)):
		if kase != 1:
			OldImg = deepcopy(NewImg)
		NewImg = cv2.resize(np.array(Image.open(FileLoc[kase]).convert("L")), (Owidth, Oheight))
		os.system("rm -rf Output/HogDEMOResult.dat")
		os.system("rm -rf Input/Inp1.dat")
		os.system("mv Input/Inp2.dat Input/Inp1.dat")
		TypeTrans.Img2Dat("df", "", "Input/Inp2.dat", NewImg)
		
		os.system("./mainpy")

		if not os.path.exists("Output/HogDEMOResult.dat"):
			continue
		ClusImg, HogDescriptor, clusMax = ReadData()
		

		if Model == "train":
			os.system("rm -rf Output/Img1.png")
			os.system("rm -rf Output/Img2.png")
			imageio.imwrite("Output/Img1.png", cv2.cvtColor(OldImg, cv2.COLOR_GRAY2BGR))
			imageio.imwrite("Output/Img2.png", cv2.cvtColor(NewImg, cv2.COLOR_GRAY2BGR))
			imgclus =  np.array([[[0, 0, 0] for n in range (Owidth)] for n in range (Oheight)])
			iro = [[255, 0 , 0], [0, 255, 0], [0, 0, 255], [128, 0, 0], [0, 128, 0], [0, 0, 128], [255, 255, 0], [255, 0, 255], [0, 255, 255], [128, 128, 0], [128, 0, 128], [0, 128, 128]]
			for i in range(0, Oheight):
				for j in range(0, Owidth):
					if ClusImg[i][j] != 0:
						imgclus[i][j] = iro[ClusImg[i][j] % 12]
			imageio.imwrite("Output/Img3.png", imgclus)
			
			Sign = GUIMain.DBSCANGUI(ClusImg, clusMax, Oheight, Owidth)

			for i in range(1, len(Sign)):
				if Sign[i] == 1:
					continue

				TrainX.append(HogDescriptor[i])
				if Sign[i] == 2:
					TrainY.append(1)
				if Sign[i] == 0:
					TrainY.append(0)


		if Model == "test":
			model = pickle.load(open("Output/model.m", 'rb'))
			TestX = []
			for i in range(1, len(HogDescriptor)):
				TestX.append(HogDescriptor[i])
			Result = model.predict(TestX)
			
			

			for i in range(0, len(Result)):
				if Result[i] == 1:
					print("WARNING!!!!")
					ImgName = "Output/WARNING/img" + str(kase) + ".png" 
					imageio.imwrite(ImgName, cv2.cvtColor(OldImg, cv2.COLOR_GRAY2BGR))
					break


	if Model == "train":
		FileName = "Output/SaveTrain.dat"
		File = open(FileName, "w")
		Str = ""
		for i in range(0, len(TrainX)):
			for j in range(0, len(TrainX[i])):
				Str += str(TrainX[i][j]) + " "
			Str += str(TrainY[i]) + "\n"
		File.write(Str)
		File.close()


	return


def trainff(FileLoc):
	TrainX = []
	TrainY = []

	File = open(FileLoc, "r")
	while 1:
		FileLine = File.readline()
		if not FileLine:
			break
		TrainX.append(FileLine.strip().split(' '))

	for i in range(0, len(TrainX)):
		for j in range(0, len(TrainX[i])):
			TrainX[i][j] = float(TrainX[i][j])
		TrainY.append(int(TrainX[i].pop()))

	clf = LinearSVC(random_state=0, tol=1e-5)	
	clf.fit(TrainX, TrainY)

	pickle.dump(clf, open("Output/model.m", 'wb'))

	print(clf.get_params([True]))

if __name__ == '__main__':
	if len(sys.argv) != 3:
		print("Parameter lost")
		os._exit(0)
	FileLoc, FileName = Init.GetSufixFile(sys.argv[2], ["png", "jpg"])
	if sys.argv[1] == "test":
		main("test", FileLoc, FileName)
	if sys.argv[1] == "train":
		main("train", FileLoc, FileName)
	if sys.argv[1] == "trainff":
		trainff(sys.argv[2])

















