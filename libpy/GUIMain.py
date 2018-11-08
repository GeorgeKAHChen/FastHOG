##=================================================================
##
##		ESC project
##		GUIMai.py
##		Copyright(c) by Kazuki Amakawa, all right reserved
##
##=================================================================
import sys
sys.path.append("/Users/kazukiamakawa/anaconda3/envs/py37/lib/python3.7/site-packages")

import pygame
from pygame.locals import *
from sys import exit

upper = 6
normal = 3


def Main(img, height, width, CellX, CellY):
	pygame.init()
	screen = pygame.display.set_mode((1400, 800), 0, 32)
	pygame.display.set_caption('Message Box Test')

	TrueX = 0
	TrueY = 0
	Sign = [[0 for n in range(width)] for n in range(height)]
	SignText = "Sign:  "
	font_family = pygame.font.SysFont('sans', 26)

	while True:
		break_switch = False
		for event in pygame.event.get():
			if event.type == QUIT:
				return Sign

			#x, y = pygame.mouse.get_pos()
			screen.set_clip(0, 0, 1400, 800)
			screen.fill((102, 204, 255))
			Enter = False

			x, y = pygame.mouse.get_pos()

			if pygame.key.get_pressed()[K_LEFT]:
				TrueX -= 1
				if TrueX < 0:
					TrueX = 0

			elif pygame.key.get_pressed()[K_RIGHT]:
				TrueX += 1
				if TrueX >= width:
					TrueX = width - 1

			elif pygame.key.get_pressed()[K_UP]:
				TrueY -= 1
				if TrueY < 0:
					TrueY = 0

			elif pygame.key.get_pressed()[K_DOWN]:
				TrueY += 1
				if TrueY >= height:
					TrueY = height - 1

			elif pygame.key.get_pressed()[K_SPACE]:
				Sign[TrueY][TrueX] = (Sign[TrueY][TrueX] + 1) % 2

			elif pygame.key.get_pressed()[K_q]:
				return Sign

			elif event.type == pygame.MOUSEBUTTONDOWN:
				if x >= 300 and x <= 300 + normal * width and y >= 50 and y <= 50 + normal * height:
					TrueX = int((x - 300) / normal)
					TrueY = int((y - 50) / normal)
					if TrueX < 0:
						TrueX = 0
					if TrueX >= width:
						TrueX = width - 1
					if TrueY < 0:
						TrueY = 0
					if TrueY >= height:
						TrueY = height - 1

			#print(TrueX, TrueY)
			text = "Point: "
			if Sign[TrueY][TrueX] == 0:
				text = str(TrueX + 1) + "   X   " + str(TrueY + 1) + "    " + SignText + "  "
			else:
				text = str(TrueX + 1) + "   X   " + str(TrueY + 1) + "    " + SignText + "* "

			#Sign area
			screen.set_clip(50, 50, 200, 50)
			screen.fill((47, 79, 79))
			screen.blit(font_family.render(text, True, (255, 255, 255)), (60, 65))
			
			#Partial image
			for Y in range(-int(CellY/2), int((CellY+1)/2)):
				for X in range(-int(CellX/2), int((CellX+1)/2)):
					screen.set_clip(100 + upper * (X + int(CellX/2)), 150 + upper * (Y + int(CellY/2)), upper, upper)
					if Y + TrueY < 0 or Y + TrueY >= height or X + TrueX < 0 or X + TrueX >= width:
						screen.fill((255, 255, 255))
					elif X == 0 and Y == 0:
						screen.fill((255, 0, 0))
					else:
						PointValue = img[Y + TrueY][X + TrueX]
						screen.fill((PointValue, PointValue, PointValue))

			#Main image
			for Y in range(0, height):
				for X in range(0, width):
					screen.set_clip(300 + normal * (X + int(CellX/2)), 50 + normal * (Y + int(CellY/2)), normal, normal)
					PointValue = img[Y][X]
					if Y == TrueY and X == TrueX:
						screen.fill((255, 0, 0))
					elif Sign[Y][X] == 1:
						screen.fill((0, 255, 0))
					else:
						screen.fill((PointValue, PointValue, PointValue))


		pygame.display.update()

	return Sign


if __name__ == '__main__':
	Main([1, 100, 1, 255], 2, 2, 2, 2)