//============================================================
//
//		FastHOG project
//		main.c
//		Copyright by KazukiAmakawa, all right reserved
//
//============================================================

#include <stdio.h>
#include <string.h>
#include <HogPixel.h>
#include <ImageIO.h>

int main(int argc, char const *argv[])
{
	unsigned char *img;
	int Owidth;
	int Oheight;
	img = ReadFromFile("Input/Inp.dat", img, &Owidth, &Oheight);

	Hog.Version = 1;

	HogInit();
	GetImage(img);
	HogImg();

	FloatWriteToFile("Output/Result.dat", HogResult, 1, Hog.nbins);
	
	return 0;
}