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

	return;
}







int AlgoMain(int Oheight, int Owidth, unsigned char *NewImg){
/*============================================================
Variable Definition
*/
	int i, j, p, q, ValX, ValY, kase;
	int ClusImg[Oheight][Owidth];
	unsigned char *PartialImg;
	PartialImg = (unsigned char *) malloc(width * height * sizeof(unsigned char));


/*============================================================
Algortihm: Differential Images
*/
	int DiffImg[Oheight][Owidth];
	int DiffTTL = 0;
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
	Write2D("Output/DiffImg.dat", Oheight, Owidth, DiffImg);
	if (DiffTTL >= Oheight * Owidth / 10){
		printf("WARNING!!");
		return 0;
	}
/*============================================================
Algorithm: DBSCAN Part
*/

	memset(ClusImg, 0, sizeof(ClusImg));
	DBSCAN(Oheight, Owidth, DiffImg, minS, ClusImg);
	//printf("%d\n", ClusterVal);
	int ClusInfo[ClusterVal + 1][4];

	for (i = 1; i < ClusterVal + 1; i ++){
		ClusInfo[i][0] = -1;
		ClusInfo[i][1] = Oheight + Owidth;
		ClusInfo[i][2] = -1;
		ClusInfo[i][3] = Oheight + Owidth;
	}

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


/*============================================================
Algorithm: HOG Part
*/
#ifdef DEMO	
	FILE *File;
	File = fopen("Output/HogDEMOResult.dat", "wb");
#endif
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
		//char tmpname[128];
		//sprintf(tmpname ,"Output/Partial_%d.dat", kase);
		//WriteToFile(tmpname, PartialImg, height, width);
		GetImage(PartialImg, height, width);
		HogMain();

#ifdef DEMO
		if(File != NULL)
		{
			for (j = 0; j < Hog.BlockLength; j ++){
				fprintf(File, "%f ", HogResult[j]);
			}
			fprintf(File, "\n");
		}
#endif
	}	


#ifdef DEMO
	fclose(File);
	File = NULL;
	Write2D("Output/ClusterImg.dat", Oheight, Owidth, ClusImg);
#endif


/*============================================================
Algorithm: SVM Classificatin
*/






/*============================================================
PostProcessing and Output


#ifdef DEMO
	fclose(File);
	File = NULL;
	Write2D("Output/ClusterImg.dat", Oheight, Owidth, ClusImg);
#endif

#ifdef DEBUG
	EndTime = clock();
	printf("Hog: %f\n", (double)(EndTime - StartTime)/ CLOCKS_PER_SEC);
	TotalEnd = clock();
	printf("Total: %f\n", (double)(TotalEnd - TotalStart)/ CLOCKS_PER_SEC);
#endif

	//FloatWriteToFile("Output/Result.dat", HogResult,  Hog.height * Hog.width, Hog.nbins);
*/
	
	return 0;
}

#endif