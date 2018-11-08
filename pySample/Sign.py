#===============================================================
#
#		FastHog project
#		Sign.py	
#		Copyright by KazukiAmakawa, all right reserved
#
#===============================================================
#import head
from PIL import Image
import numpy as np
import os
from scipy import misc
import cv2

from libGUI import GUIMain
from libpy import TypeTrans
from libpy import Init


width = 256
height = 144

def Main(Imgs, FileName):
	os.system("rm -rf  Output/HogSVM")
	os.system("mkdir Output/HogSVM")
	os.system("mkdir Output/HogSVM/img")
	os.system("mkdir Output/HogSVM/Sign")
	for i in range(0, len(Imgs)):
		img = cv2.resize(np.array(Image.open(Imgs[i]).convert("L")), (width, height))

		Sign = GUIMain.Main(img, height, width, 25, 25)
		Sign = 255 * np.array(Sign)
		misc.imsave("Output/HogSVM/img/" + FileName[i] + ".png", img)
		TypeTrans.Result2Dat("Output/HogSVM/Sign/" + FileName[i] + ".dat", Sign)


if __name__ == '__main__':
	FileLoc, FileName = Init.GetSufixFile("Input/SampleInput", ["jpg"])
	print(FileLoc[0])
	Main(FileLoc, FileName)