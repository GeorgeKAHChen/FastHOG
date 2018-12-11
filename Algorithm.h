/*=================================================================
//
//		Fast Hog project
//		Algorithm.h
//		Copyright(c) by Kazuki Amakawa, all right reserved
//
=================================================================*/

#include <stdio.h>
#include <string.h>
#include <time.h>

#include "DBSCAN.h"
#include "Hog.h"

#include "ImageIO.h"
#include "yuv-predict.h"

#ifndef DEFALGO
#define DEFALGO

//#define DEBUG
#define DEMO

unsigned char *OldImg;

/*============================================================
Parameter
*/
int epision = 4;
int minS = 25;
int NegativeVal = 50;
int height = 72;
int width = 36;




void AlgoInitial(int Oheight, int Owidth, unsigned char *yuvbuff){	
/*============================================================
Algorithm: Initialization
*/
	OldImg = (unsigned char *) malloc(Oheight * Owidth);
	memcpy(OldImg, yuvbuff, Oheight * Owidth);

	DBSCANInit(epision, Oheight, Owidth);		//Initial DBSCAN
	Hog.width = width;
	Hog.BlockX = width;
	Hog.height = height;
	Hog.BlockY = height;
	HogInit();									//Initial HOG

	svm_Initial(Hog.BlockTtl * Hog.BlockLength, "Input/model.m");

	return;
}







int AlgoMain(int Oheight, int Owidth, unsigned char *NewImg){
/*============================================================
Variable Definition
*/
	int i, j, p, q, ValX, ValY, kase;
	int DiffTTL = 0;
	int HaveHuman = 0;
	
	//Define cluster image and size and initial
	int (*ClusImg)[Owidth] = NULL;
	ClusImg = (int (*)[Owidth]) malloc(Oheight * Owidth * sizeof(int));
	
	for (i = 0; i < Oheight; i ++)
		for (j = 0; j < Owidth; j ++)			ClusImg[i][j] = 0;

	//Define differential image and size
	int (*DiffImg)[Owidth] = NULL;
	DiffImg = (int (*)[Owidth]) malloc(Oheight * Owidth * sizeof(int));	

	//Define partial image for hog and size
	unsigned char *PartialImg = NULL;
	PartialImg = (unsigned char *) malloc(width * height * sizeof(unsigned char));
	
	//Define cluster information
	int (*ClusInfo)[4] = NULL;


/*============================================================
Algortihm: Differential Images
*/
	//Differential Image
	for (i = 0; i < Oheight; i ++){
		for (j = 0; j < Owidth; j ++){
			if ((int)OldImg[i * Owidth + j] - (int)NewImg[i * Owidth + j] > NegativeVal || 
				(int)OldImg[i * Owidth + j] - (int)NewImg[i * Owidth + j] < -NegativeVal ){
												DiffImg[i][j] = 1;
												DiffTTL += 1;
			}
			else								DiffImg[i][j] = 0;
		}
	}
	
	//If a image have too many different pixel, break!
	if (DiffTTL >= Oheight * Owidth / 20){
		printf("WARNING!!");
		goto AlgorithmEnd;
	}



/*============================================================
Algorithm: DBSCAN Part
*/
	//Main DBSCAN algorithm
	DBSCAN(Oheight, Owidth, DiffImg, minS, ClusImg);

	//Size and Initial the Cluster infromation data array
	ClusInfo = (int (*)[4]) malloc(4 * (ClusterVal + 1) * sizeof(int));

	for (i = 1; i < ClusterVal + 1; i ++){
		ClusInfo[i][0] = -1;
		ClusInfo[i][1] = Oheight + Owidth;
		ClusInfo[i][2] = -1;
		ClusInfo[i][3] = Oheight + Owidth;
	}

	//Get the cluster information
	for (i = 0; i < Oheight; i ++){
		for (j = 0; j < Owidth; j ++){
			if (ClusImg[i][j] != 0){
				if (ClusInfo[ClusImg[i][j]][0] < i)		ClusInfo[ClusImg[i][j]][0] = i;
				if (ClusInfo[ClusImg[i][j]][1] > i)		ClusInfo[ClusImg[i][j]][1] = i;
				if (ClusInfo[ClusImg[i][j]][2] < j)		ClusInfo[ClusImg[i][j]][2] = j;
				if (ClusInfo[ClusImg[i][j]][3] > j)		ClusInfo[ClusImg[i][j]][3] = j;
			}
		}
	}

	for (i = 1; i < ClusterVal + 1; i ++)
		printf("%d  %d  %d  %d\n", ClusInfo[i][0], ClusInfo[i][1], ClusInfo[i][2], ClusInfo[i][3]);

/*============================================================
Algorithm: HOG + SVM Part
*/
	for (kase = 1; kase < ClusterVal + 1; kase ++){
		int LengY = (int) (ClusInfo[kase][0] - ClusInfo[kase][1]) / height;
		int LengX = (int) (ClusInfo[kase][2] - ClusInfo[kase][3]) / width;
		if (LengY <= 0) 						LengY = 1;
		if (LengX <= 0) 						LengX = 1;

		for (i = 0; i < Hog.height; i ++){
			for(j = 0; j < Hog.width; j ++){
				ValY = (int) i * LengY + ClusInfo[kase][1];
				ValX = (int) j * LengX + ClusInfo[kase][3];
				PartialImg[i * Hog.width + j] = (unsigned char)Hog.GammaTable[(int)NewImg[ValY * Owidth + ValX]];
			}
		}
		GetImage(PartialImg, height, width);
		HogMain();
		
		if (read_from_memory(Hog.BlockTtl * Hog.BlockLength, HogResult) == 1){
			HaveHuman = 1;
			break;
		}
	}	


AlgorithmEnd:
	if (ClusImg)				free(ClusImg);
	if (DiffImg)				free(DiffImg);
	if (PartialImg)				free(PartialImg);
	if (ClusInfo)				free(ClusInfo);
	memcpy(OldImg, NewImg, sizeof(NewImg));
	return 0;
}

#endif
