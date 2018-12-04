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


def Dat2Img(Model, InputFile, OutputFile, img1):
	img = []
	if Model[0] == "f":
		File = open(InputFile, "r")
		
		FileLine = File.readline()
		width = 0
		height = 0
		Str = ""
		Val = []

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
						for j in range(0, len(Str)):
							if Str[j] == ".":
								Val.append(float(Str))
								Str = ""
								break
						if Str != "":
							Val.append(int(Str))
							Str = ""
						
						continue

				Str += FileLine[i]

			img.append(Val)
	else:
		img = img1
	
	if Model[1] == "f":
		#img *= 255
		misc.imsave(OutputFile, np.array(img))
		
	return img



def yuv420_to_rgb888(width, height, yuv):
	if (width % 4) or (height % 4):
		raise Exception("width and height must be multiples of 4")
	rgb_bytes = bytearray(width*height*3)

	red_index = 0
	green_index = 1
	blue_index = 2
	y_index = 0
	for row in range(0,height):
		u_index = width * height + (row//2)*(width//2)
		v_index = u_index + (width*height)//4
		for column in range(0,width):
			Y = yuv[y_index]
			U = yuv[u_index]
			V = yuv[v_index]
			C = (Y - 16) * 298
			D = U - 128
			E = V - 128
			R = (C + 409*E + 128) // 256
			G = (C - 100*D - 208*E + 128) // 256
			B = (C + 516 * D + 128) // 256
			R = 255 if (R > 255) else (0 if (R < 0) else R)
			G = 255 if (G > 255) else (0 if (G < 0) else G)
			B = 255 if (B > 255) else (0 if (B < 0) else B)
			rgb_bytes[red_index] = R
			rgb_bytes[green_index] = G
			rgb_bytes[blue_index] = B
			u_index += (column % 2)
			v_index += (column % 2)
			y_index += 1
			red_index += 3
			green_index += 3
			blue_index += 3
	return rgb_bytes



def yuv2rgb(FileLoc, FileName, width, height):
	from PIL import Image
	import os
	os.system("rm -rf tmpout")
	os.system("mkdir tmpout")
	for kase in range(0, len(FileLoc)):

		f = open(FileLoc[kase], "rb")
		yuv = f.read()
		f.close()
		rgb_bytes = yuv420_to_rgb888(width, height, yuv)
		img = Image.frombytes("RGB", (width, height), bytes(rgb_bytes))
		img.save("tmpout/" + FileName[kase] + ".jpg", "JPEG")
		img.close()

