#===============================================================
#
#		FastHog project
#		Train.py	
#		Copyright by KazukiAmakawa, all right reserved
#
#===============================================================
#import head
from PIL import Image
import numpy as np
import os
from scipy import misc
import cv2

from sklearn.externals import joblib
from sklearn import svm

from libpy import TypeTrans
from libpy import Init


def HogCalculate(FileLoc, FileName):
	os.system("rm -rf Output/HogSVM/HogResult")
	os.system("rm -rf Output/HogSVM/DatImg")
	os.system("mkdir Output/HogSVM/HogResult")
	os.system("mkdir Output/HogSVM/DatImg")
	os.system("rm -rf ./HogMain")
	os.system("gcc -I ./lib ./HogMain.c -o HogMain -v")

	for kase in range(0, len(FileLoc)):
		img = np.array(Image.open(FileLoc[kase]).convert("L"))
		TypeTrans.Result2Dat("Output/HogSVM/DatImg/" + FileName[kase] + ".dat", img)

		os.system("cp Output/HogSVM/DatImg/" + FileName[kase] + ".dat" + " Input/Inp.dat")
		os.system("./HogMain")
		os.system("mv Output/Result.dat Output/HogSVM/HogResult/" + FileName[kase] + ".dat")


def SVMTrain(FileLoc, FileName):
	os.system("rm -rf Output/HogSVM/Model")
	os.system("mkdir Output/HogSVM/Model")
	
	TrainX = []
	TrainY = []
	
	for kase in range(0, len(FileName)):
		HogFile = "Output/HogSVM/HogResult/" + FileName[kase] + ".dat"
		SignFile = "Output/HogSVM/Sign/" + FileName[kase] + ".dat"

		HogDescriptor = Init.ReadFloat(HogFile)
		SignArr = Init.ReadFloat(SignFile)

		Result = []

		for i in range(0, len(SignArr)):
			for j in range(0, len(SignArr[i])):
				Result.append(int(SignArr[i][j]))
		Result = np.array(Result)
		print(len(HogDescriptor), len(Result))

		for i in range(0, len(HogDescriptor)):
			TrainX.append(HogDescriptor[i])
			TrainY.append(Result[i])

	clf = svm.SVC()
	clf.fit(TrainX, TrainY)

	joblib.dump(clf, "Output/HogSVM/Model/model.m")



if __name__ == '__main__':
	FileLoc, FileName = Init.GetSufixFile("Output/HogSVM/img", ["png"])
	HogCalculate(FileLoc, FileName)

	SVMTrain(FileLoc, FileName)

	#SVM train and save the model



	
