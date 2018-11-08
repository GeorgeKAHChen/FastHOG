#===============================================================
#
#		FastHog project
#		TmpMain.py	
#		Copyright by KazukiAmakawa, all right reserved
#
#===============================================================
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os
import os.path
import math
import matplotlib.patches as patches
import imageio
from collections import deque
from PIL import ImageFilter
from copy import deepcopy
import cv2 

from sklearn.cluster import DBSCAN
from sklearn.svm import SVC
import datetime

from libpy import Init
from libpy import TypeTrans

from sklearn.externals import joblib
from sklearn import svm

import time

ThsNeg = 10

samples = 25
episilon = 4

CellX = 9
CellY = 16

ImgWidth = 144
ImgHeight = 256

ProbThs = 0.5



def Main(Files, filename):
	OldImg = cv2.resize(np.array(Image.open(Files[0]).convert("L")), (256, 144))
	print("\t\t\tDBSCAN\t\tHog\t\t")
	clf = joblib.load("Output/HogSVM/Model/model.m")
	HogImg = [[0 for n in range(CellX)] for n in range(CellY)]

	for kase in range(1, len(Files)):
		print(filename[kase], end = "\t")
		NewImg = cv2.resize(np.array(Image.open(Files[kase]).convert("L")), (256, 144))

		"""
		Differential Part & DBSCAN Part
		"""
		starttime = datetime.datetime.now()
		ClusImg1= np.array([[0 for n in range(len(NewImg[0]))] for n in range(len(NewImg))])
		ClusSet = []
		for i in range(0, len(NewImg)):
			for j in range(0, len(NewImg[i])):
				#print(NewImg[i][j], OldImg[i][j], int(NewImg[i][j]) - int(OldImg[i][j]))
				if int(NewImg[i][j]) - int(OldImg[i][j]) > ThsNeg or int(NewImg[i][j]) - int(OldImg[i][j]) < -ThsNeg:
					ClusImg1[i][j] = 1
					ClusSet.append([i, j])
		#print()
		#print(len(ClusSet))
		clustering = DBSCAN(eps=episilon, min_samples = samples).fit(ClusSet)
		Result = clustering.labels_


		ClusImg = np.array([[[0, 0, 0] for n in range(ImgHeight)] for n in range(ImgWidth)])
		for i in range(0, ImgWidth):
			for j in range(0, ImgHeight):
				ClusImg[i][j][0] = NewImg[i][j]
				ClusImg[i][j][1] = NewImg[i][j]
				ClusImg[i][j][2] = NewImg[i][j]

		for i in range(0, len(ClusSet)):
			if Result[i] != -1:
				ClusImg[ClusSet[i][0]][ClusSet[i][1]][0] = 255

		TypeTrans.Img2Dat("df", "", "Input/Inp1.dat", ClusImg1)

		imageio.imwrite("tmpout/Img1.png", OldImg)
		imageio.imwrite("tmpout/Img2.png", NewImg)
		imageio.imwrite("tmpout/ClusImg.png", ClusImg)
		imageio.imwrite("tmpout/NegImg.png", ClusImg1)
		
		TypeTrans.Img2Dat("df", "", "Input/Inp1.dat", OldImg)
		TypeTrans.Img2Dat("df", "", "Input/Inp2.dat", NewImg)

		endtime = datetime.datetime.now()
		print(endtime - starttime, end = "\t")

		return

		"""
		Hog Descriptor & SVM Classification
		
		starttime = datetime.datetime.now()

		TTL = max(Result)
		Probability = [0 for n in range(TTL + 1)]
		Size = [0 for n in range(TTL + 1)]
		for i in range(0, len(ClusSet)):
			#print(i)
			if Result[i] == -1:
				continue

			for p in range(-int(CellY/2), int((CellY + 1) / 2)):
				for q in range(-int(CellX/2), int((CellX + 1) / 2)):
					Y = ClusSet[i][0] + p
					X = ClusSet[i][1] + q
					loc = 255
					if X > 0 and X < ImgWidth and Y > 0 and Y < ImgHeight:
						loc = NewImg[X][Y]

					HogImg[p+int(CellY/2)][q+int(CellX/2)] = loc

			TypeTrans.Result2Dat("Input/Inp.dat", HogImg)
			os.system("./Hog")
			
			HogResult = Init.ReadFloat("Output/Result.dat")
			
			Classify = clf.predict(HogResult)[0]

			Probability[Result[i]] += Classify
			Size[Result[i]] += 1

		endtime = datetime.datetime.now()
		print(endtime - starttime, end = "\t")

		for i in range(0, len(Probability)):
			Probability[i] = Probability[i] / Size[i]
			if Probability[i] >= ProbThs:
				print("WARNING!!")
				break
			else:
				print()
				continue
		
		OldImg = deepcopy(NewImg)
	misc.imsave(filename, img)

	"""


	"""
	Statistic Decision
	"""





if __name__ == '__main__':
	FileLoc, FileName = Init.GetSufixFile("Input/SampleInput", ["jpg"])
	Main(FileLoc, FileName)











