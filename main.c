//============================================================
//
//		FastHOG project
//		main.c
//		Copyright by KazukiAmakawa, all right reserved
//
//============================================================

#include <stdio.h>
#include <string.h>
#include <Algorithm.h>
#include <ImageIO.h>

#define DEBUG
#define DEMO

int main(int argc, char const *argv[])
{
	unsigned char *img1;
	unsigned char *img2;
	int Oheight, Owidth;
	img1 = ReadFromFile("Input/Inp1.dat", img1, &Oheight, &Owidth);
	img2 = ReadFromFile("Input/Inp2.dat", img2, &Oheight, &Owidth);
	//printf("%d  %d\n", Oheight, Owidth);
	AlgoInitial(Oheight, Owidth, img1);
	AlgoMain(Oheight, Owidth, img2);
	return 0;
}