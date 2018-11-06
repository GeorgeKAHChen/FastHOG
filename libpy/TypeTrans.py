##=================================================================
##
##		ESC project
##		TypeTrans.py
##		Copyright(c) by Kazuki Amakawa, all right reserved
##
##=================================================================

from PIL import Image
import numpy as np
import os
import os.path
import math
from scipy import misc
from collections import deque
from PIL import ImageFilter
from copy import deepcopy

from libpy import Init

def Img2Dat(Model, InputFile, OutputFile, img):
	if Model[0] == "f":
		img = np.array(Image.open(location).convert("L"))

	if Model[1] == "f":
		String = "1 " + str(len(img)) + " " + str(len(img[0])) + "\n"
		for i in range(0, len(img)):
			for j in range(0, len(img[i])):
				String += str(img[i][j]) + " "
			String += "\n"

		File = open(OutputFile, "w")
		File.write(String)
		File.close()

	return img


def Dat2Img(Model, InputFile, OutputFile, img):
	if Model[0] == "f":
		File = open(InputFile, "r")
		
		FileLine = File.readline()
		width = 0
		height = 0
		Str = ""
		Val = []
		img = []

		while 1:
			FileLine = File.readline()
			if not FileLine:
				break
			Val = []
			for i in range(0, len(FileLine)):
				if FileLine[i] == " " or i + 1 == len(FileLine) or FileLine[i] == "\n":
					if len(Str) == 0:
						continue
					if Str == "nan":
						Val.append(0)
					else:
						Val.append(float(Str))
						Str = ""
						continue

				Str += FileLine[i]

			img.append(Val)
	
	if Model[1] == "f":
		img *= 255
		misc.imsave(filename, np.array(img))
		
	return img


