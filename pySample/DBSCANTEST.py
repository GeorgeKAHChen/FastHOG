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

import DBSCANDemo

ThsNeg = 10

samples = 25
episilon = 4

CellX = 9
CellY = 16

ImgHeight = 144
ImgWidth = 256

ProbThs = 0.5



def Main(Files, filename):
	OldImg = cv2.resize(np.array(Image.open(Files[0]).convert("L")), (ImgWidth, ImgHeight))
	DBSCANTABLE = DBSCANDemo.Initial()
	print(len(DBSCANTABLE))
	for kase in range(1, len(Files)):
		print(filename[kase], end = "\t")
		NewImg = cv2.resize(np.array(Image.open(Files[kase]).convert("L")), (ImgWidth, ImgHeight))

		"""
		Differential Part & DBSCAN Part
		"""
		ClusImg1 = np.array([[0 for n in range(ImgWidth)] for n in range(ImgHeight)])

		

		for i in range(0, len(NewImg)):
			for j in range(0, len(NewImg[i])):
				if int(NewImg[i][j]) - int(OldImg[i][j]) > ThsNeg or int(NewImg[i][j]) - int(OldImg[i][j]) < -ThsNeg:
					ClusImg1[i][j] = 1

		starttime = datetime.datetime.now()
		CLUSIMG, OUTERNODE, TOTALCLUS = DBSCANDemo.DBSCAN(ImgHeight, ImgWidth, ClusImg1, DBSCANTABLE)

		endtime = datetime.datetime.now()
		print(endtime - starttime, end = "\t")

		ClusImg = np.array([[[0, 0, 0] for n in range(ImgWidth)] for n in range(ImgHeight)])
		for i in range(0, ImgHeight):
			for j in range(0, ImgWidth):
				if CLUSIMG[i][j] != 0:
					ClusImg[i][j][0] = 255
					continue
				ClusImg[i][j][0] = NewImg[i][j]
				ClusImg[i][j][1] = NewImg[i][j]
				ClusImg[i][j][2] = NewImg[i][j]

		for i in range(0 , len(OUTERNODE)):
			if CLUSIMG[OUTERNODE[i][0]][OUTERNODE[i][1]] == 0:
				ClusImg[OUTERNODE[i][0]][OUTERNODE[i][1]][0] = 0
				ClusImg[OUTERNODE[i][0]][OUTERNODE[i][1]][1] = 255
				ClusImg[OUTERNODE[i][0]][OUTERNODE[i][1]][2] = 0
				continue

			ClusImg[OUTERNODE[i][0]][OUTERNODE[i][1]][0] = 0
			ClusImg[OUTERNODE[i][0]][OUTERNODE[i][1]][1] = 0
			ClusImg[OUTERNODE[i][0]][OUTERNODE[i][1]][2] = 255
		
		imageio.imwrite("tmpout/Img1.png", OldImg)
		imageio.imwrite("tmpout/Img2.png", NewImg)
		imageio.imwrite("tmpout/ClusImg.png", ClusImg)
		imageio.imwrite("tmpout/NegImg.png", ClusImg1)


		return





if __name__ == '__main__':
	FileLoc, FileName = Init.GetSufixFile("Input/SampleInput", ["jpg"])
	Main(FileLoc, FileName)











