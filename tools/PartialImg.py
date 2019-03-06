#===============================================================
#
#		FastHog project
#		PartialImg.py	
#		Copyright by KazukiAmakawa, all right reserved
#
#===============================================================
#Please determine train data location before training and sign
#==============================
#Parameter start
#LocInit = "./Data/NVP/s1"
LocInit = "./Data/rgbDay/"
FileSuf = ".jpg"
ThresDis = 50
episilon = 50
minS = 5000
#Parameter finish


#import headfiles
import os
from PIL import Image
import numpy as np
import imageio
from copy import deepcopy
import math


#Global Parameter, do NOT change!!



def DBSCANInit(episilon, height, width):
	AreaTable = [[0 for n in range(2 * episilon + 1)] for n in range(2 * episilon + 1)]
	WidthImg = width

	SizeOfTable = 0
	for i in range(0, 2 * episilon + 1):
		for j in range(0, 2 * episilon + 1):
			if i == episilon and j == episilon:
				continue

			if math.sqrt(pow(i - episilon, 2) + pow(j - episilon, 2)) <= episilon:
				SizeOfTable += 1
				AreaTable[i][j] = 1

	DBSCANTable = []
	Val = 0

	for i in range(0, 2 * episilon + 1):
		for j in range(0, 2 * episilon + 1):
			if AreaTable[i][j] == 1:
				DBSCANTable.append(i - episilon)
				DBSCANTable.append(j - episilon)
				Val += 1

	return DBSCANTable


def DBSCAN(InpImg, minS, DBSCANTable, height, width):
	#Initial variable and array
	LabelImg = [[0 for n in range(width)] for n in range(height)]
	ClusterVal = 0

	#For cluster and DFS
	Stack = []

	for i in range(0, height):
		for j in range(0, width):
			if InpImg[i][j] == 0:
				continue
			if LabelImg[i][j] != 0:
				continue

			"""
			Find inner node
			"""
			Point = 0
			Inner = 0
			willCluster = 0
			
			#That means, if a node have neighbour node >= minS, then it will 
			#build a new cluster
			for k in range(0, int(len(DBSCANTable) / 2 + 0.5)):
				ValY = i + DBSCANTable[2 * k]
				ValX = j + DBSCANTable[2 * k + 1]
				if ValY < 0 or ValY >= height or ValX < 0 or ValX >= width:
					continue

				if InpImg[ValY][ValX] == 1:
					Point += 1

				if Point >= minS:
					Inner = 1
					if LabelImg[i][j] == 0:
						willCluster = 1;
						break;

					else:
						break

			"""
			New cluster
			"""
			if willCluster:
				#Using DFS to find connected neighbour in episilon region
				Stack.append([i, j])
				ClusterVal += 1

				while 1:
					iNew, jNew = Stack.pop()
					LabelImg[iNew][jNew] = ClusterVal

					for k in range(0, len(DBSCANTable) / 2):
						ValY = iNew + DBSCANTable[2 * k]
						ValX = jNew + DBSCANTable[2 * k + 1]

						#Out of boundary
						if ValY < 0 or ValY >= height or ValX < 0 or ValX >= width:
							continue

						#Not have variable
						if InpImg[ValY][ValX] == 0:
							continue

						#Labeled
						if LabelImg[ValY][ValX] >= 1:
							continue

						#Build cluster
						if InpImg[ValY][ValX] == 1:
							noStack = 0
							for l in range(0, len(Stack)):
								if Stack[l][0] == ValY and Stack[l][1] == ValX: 
									noStack = 1
									break
								
							if noStack == 0:
								Stack.append(ValY, ValX)

					if (len(Stack) == 0):
						break


	return LabelImg, ClusterVal


def main():
	os.system("clear")
	#Get file list
	MinFile = 999999
	MaxFile = -1
	for root, dirs, files in os.walk(LocInit):
		for i in range(0, len(files)):
			Val = 0
			for j in range(0, len(files[i])):
				if ord(files[i][j]) >= ord("0") and ord(files[i][j]) <= ord("9"):
					Val = Val * 10 + int(files[i][j])

			MinFile = min(Val, MinFile)
			MaxFile = max(Val, MaxFile)

	#Import initial files
	FileName = LocInit + str(MinFile) + FileSuf
	img1 = np.array(Image.open(FileName).convert("L"))
	height = len(img1)
	width = len(img1[1])

	#Initial DBSCAN 
	DBSCANTable = DBSCANInit(episilon, height, width)

	print("Algorithm initial finished")
	print("Inital image read")

	for kase in range(MinFile + 1, MaxFile + 1):
		print("Image: " + str(kase) + ", Total: " + str(MaxFile) + ", Processing: " + str((kase - MinFile - 1) / (MaxFile - MinFile)), end = "\r")
		#Copy image if it is not first time looping
		if kase != MinFile + 1:
			img1 = deepcopy(img2)

		#Import files
		FileName = LocInit + str(kase) + FileSuf
		img2 = np.array(Image.open(FileName).convert("L"))

		#Differential images
		DisImg = [[0 for n in range(len(img1[0]))] for n in range(len(img1))]
		for i in range(0, height):
			for j in range(0, width):
				if int(img1[i][j]) - int(img2[i][j]) >= ThresDis or int(img1[i][j]) - int(img2[i][j]) <= -ThresDis:
					DisImg[i][j] = 1
		
		#DBSCAN Cluster
		ClusImg, MaxClus = DBSCAN(DisImg, minS, DBSCANTable, height, width)

		#Get Bounding Box and Save Files
		BoxData = [[99999999, 99999999, -1, -1] for n in range(MaxClus)]
		for i in range(0, len(ClusImg)):
			for j in range(0, len(ClusImg[i])):
				if ClusImg[i][j] == 0:
					continue

				for k in range(0, len(BoundingClus)):
					if ClusImg[i][j] == BoundingClus[k]:
						BoxData[k][0] = min(i, BoxData[k][0])
						BoxData[k][1] = min(j, BoxData[k][1])
						BoxData[k][2] = max(i, BoxData[k][2])
						BoxData[k][3] = max(j, BoxData[k][3])

		#Folder clear
		if len(BoxData) > 0:
			if os.path.exists("./Output/TrainImg"):
				os.system("mv ./Output/TrainImg ./Output/Olds")
			os.system("mkdir ./Output/TrainImg")

		#Get bounding box and saving
		for k in range(0, len(BoxData)):
			leftx = BoxData[k][0]
			lefty = BoxData[k][1]
			rightx = BoxData[k][2]
			righty = BoxData[k][3]
			Saveimg1 = [[0 for n in range(righty - lefty)] for n in range(rightx - leftx)]
			Saveimg2 = [[0 for n in range(righty - lefty)] for n in range(rightx - leftx)]
			for i in range(len(leftx),  len(rightx) + 1):
				for j in range(len(lefty),  len(righty) + 1):
					Saveimg1[i - len(leftx)][j - len(lefty)] = int(img1[i][j])
					Saveimg2[i - len(leftx)][j - len(lefty)] = int(img2[i][j])
			Saveimg1 = np.array(img.resize((72, 36), Image.ANTIALIAS))
			Saveimg2 = np.array(img.resize((72, 36), Image.ANTIALIAS))
			imageio.imwrite("./Output/TrainImg/1-" + str(kase - 1) + "-" + str(kase) + "-" + str(k) + ".png" , Saveimg1)
			imageio.imwrite("./Output/TrainImg/2-" + str(kase - 1) + "-" + str(kase) + "-" + str(k) + ".png" , Saveimg2)



if __name__ == '__main__':
	main()






