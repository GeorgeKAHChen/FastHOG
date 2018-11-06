//============================================================
//
//		FastHOG project
//		main.c
//		Copyright by KazukiAmakawa, all right reserved
//
//============================================================

#include <stdio.h>
#include <string.h>
#include <DBSCAN.h>
#include <ImageIO.h>

#include <time.h>

int main(int argc, char const *argv[])
{
	/*
	Parameter
	*/
	int epision = 4;
	int minS = 25;
	int NegativeVal = 10;
	int Oheight = 144;
	int Owidth = 256;
	int height = 9;
	int width = 16;


	/*
	Variable Definition
	*/
	unsigned char *img;
	int i, j, p, q, ValX, ValY;
	int ClusImg[height][width];
	clock_t StartTime, EndTime;
	

	/*
	Algorithm: Initialization
	*/
	img1 = ReadFromFile("Input/Inp1.dat", img, &Owidth, &Oheight);

	DBSCANInit(epision, Oheight, Owidth);		//Initial DBSCAN
	Hog.width = width;
	Hog.height = height;
	HogInit();									//Initial HOG
	

	/*
	Algortihm: Differential Images
	*/
	img2 = ReadFromFile("Input/Inp1.dat", img, &Owidth, &Oheight);
	StartTime = clock();
	int DiffImg[Oheight][Owidth];
	for (i = 0; i < Oheight; i ++){
		for (j = 0; j < Owidth; j ++){
			if ((int)img1[i * Owidth + j] - (int)img2[i * Owidth + j] >= NegativeVal || 
				(int)img1[i * Owidth + j] - (int)img2[i * Owidth + j] <= -NegativeVal )
												DiffImg[i][j] = 1;
			else								DiffImg[i][j] = 0;
		}
	}
	EndTime = clock();
	printf("Differential: %f\n", (double)(EndTime - StartTime)/ CLOCKS_PER_SEC);
	
	
	/*
	Algorithm: DBSCAN Part
	*/
	StartTime = clock();
	memset(ClusImg, 0, sizeof(ClusImg));
	DBSCAN(Oheight, Owidth, DiffImg, minS, ClusImg);
	printf("ClusterVal: %d\n", ClusterVal);
	EndTime = clock();
	printf("Cluster: %f\n", (double)(EndTime - StartTime)/ CLOCKS_PER_SEC);
	
		
	/*
	Algorithm: HOG Part
	*/
	for (i = 0; i < TotalOutNode; i ++){
		unsigned char PartialImg;
		for (p = -height/2; p < (height+1)/2; p ++){
			for (q = -width/2; q < (width+1)/2; q ++){
				ValY = OuterNode[i][0] + p;
				ValX = OuterNode[i][0] + p;
				if (ValY < 0 || ValY >= Oheight || ValX < 0 || ValX >= Owidth)
												PartialImg[(p + height/2) * width + q + width/2] = 0;
				else							PartialImg[(p + height/2) * width + q + width/2] = img2[ValY * Oheight + ValX];
			}
		}

		GetImage(img);
		HogImg();
	}
	
	FloatWriteToFile("Output/Result.dat", HogResult,  Hog.height * Hog.width, Hog.nbins);
	
	return 0;
}