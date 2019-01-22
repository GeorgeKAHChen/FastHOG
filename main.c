//============================================================
//
//		FastHOG project
//		main.c
//		Copyright by KazukiAmakawa, all right reserved
//
//============================================================

#include <stdio.h>
#include <string.h>
#include "Algorithm.h"
#include "ImageIO.h"
#include <dlfcn.h>
#include <time.h>

#define DEBUG
#define DEMO

int main(int argc, char const *argv[])
{
	printf("Compile succeed\n");
	unsigned char *img1;
	unsigned char *img2;
	int Oheight, Owidth;
	img1 = ReadFromFile("tmpInp/Inp1.dat", img1, &Oheight, &Owidth);
	img2 = ReadFromFile("Input/Inp2.dat", img2, &Oheight, &Owidth);
	//printf("%d  %d\n", Oheight, Owidth);
	AlgoInitial(Oheight, Owidth, img1);
    clock_t startTime,endTime;
    startTime = clock();
    AlgoMain(Oheight, Owidth, img2);
    endTime = clock();

    printf("%f", (double)(endTime - startTime) / CLOCKS_PER_SEC);
	return 0;
}
