/*=================================================================
//
//		ESC project
//		Hog algorithm part, Hog in C
//		Copyright(c) by Kazuki Amakawa, all right reserved
//
=================================================================*/

#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h> 
#include "ImageIO.h"

#define DEBUG
#ifndef HogINITIAL
/*
Define of Global parameter
*/
float *HogResult;
float *Gradient;
float *Angle;
#define HogINITIAL
#define PI 3.1415926535897932384626
#endif


struct HOGDescriptor
{
	/*
	Parameter in HOG
	Once you changed these parameters of Hog, it is necessary to run the init function again
	*/

	float Gamma;
	int height, width;
	int BlockY, BlockX;
	int StrideY, StrideX;
	int CellY, CellX;
	int nbins;
	int BlockOutput;
	
	
	int BlockLength;
	int BlockTtl;
	float GammaTable[256];
	//Gamma, width, height, BlockY, BlockX, StrideY, StrideX, CellY, CellX, nbins, Ouptput
}Hog = 
	//{ 0.5  , 36   , 18    , 36    , 18    , 9      , 4      , 18   , 9    , 9    , 0      };
	  { 0.5  , 72   , 36    , 72    , 36    , 12     , 6      , 18   , 9    , 9    , 0      };



int HogInit()
{
	/*
	This function is initila of hog algorithm,
	It will initial values in HOGDescriptor and get memory location of Result
	Once you changed the parameter of Hog, it is necessary to run this init function again
	*/
	int i;
	float f;
	for (i = 0; i < 256; i ++){
		f = (i + 0.5) / 256;
		f = (float) pow(f, Hog.Gamma);
		Hog.GammaTable[i] = (int)(f * 256 - 0.5);
	}

	if (Hog.width % Hog.BlockX != 0 && Hog.height % Hog.BlockY != 0)	return -1;
	if (Hog.BlockX % Hog.CellX != 0 && Hog.BlockY % Hog.CellY != 0)		return -2;
	
	Hog.BlockLength = (int)Hog.BlockX / Hog.CellX * Hog.BlockY / Hog.CellY * Hog.nbins;
	Hog.BlockTtl = (int)(((Hog.width - Hog.BlockX) / Hog.StrideX) + 1) * (((Hog.height - Hog.BlockY) / Hog.StrideY) + 1) ;
	//HogResult = (float *)malloc(Hog.BlockLength * Hog.BlockTtl);
	HogResult = (float *)malloc(Hog.BlockTtl * Hog.BlockLength * sizeof(HogResult));
	
	Gradient = (float *)malloc(Hog.width * Hog.height * sizeof(float));
	Angle = (float *)malloc(Hog.width * Hog.height * sizeof(float));
	if (Hog.BlockOutput != 0 && Hog.BlockOutput != 1)					Hog.BlockOutput = 0;
	
	return 0;
}


void GetImage(unsigned char *img, int Oheight, int Owidth)
{
	int i, j;
	/*
	Get gradient figure and angle
	*/
	float ValX, ValY;
	int x1, x2, y1, y2;
	for (i = 0; i < Hog.height; i ++){
		for (j = 0; j < Hog.width; j ++){
			if(j - 1 < 0)					x1 = 0;
			else							x1 = (int)img[i * Hog.width + j - 1];
			
			if(j + 1 >= Hog.width)			x2 = 0;
			else							x2 = (int)img[i * Hog.width + j + 1];

			if(i - 1 < 0)					y1 = 0;
			else							y1 = (int)img[(i-1) * Hog.width + j];

			if(i + 1 >= Hog.height)			y2 = 0;
			else							y2 = (int)img[(i+1) * Hog.width + j];

			ValX = x2 - x1;
			ValY = y2 - y1;
			
			if (ValY == 0 || ValX == 0)		Angle[i * Hog.width + j] = 0;
			else							Angle[i * Hog.width + j] = atan(ValY / ValX) * 180 / PI;
			Gradient[i * Hog.width + j] = sqrt(ValX * ValX + ValY * ValY)
			;
		}
	}

	return ;
}


void HogMain(){
	int i = 0;
	int j = 0;
	int kase = 0;
	int ttl = 0;
	int p, q, m, n, r, point, Local;
	float Step = 180 / Hog.nbins;
	float BlockSum, Val, Ang;
	float Histogram[Hog.nbins];
	
	while (1){
		if (j + Hog.BlockX > Hog.width){
			j = 0;
			i += Hog.StrideY;
		}
		if (i + Hog.BlockY > Hog.height)			break;
		ttl ++;

		//Initial block valiables
		p = 0;
		q = 0;
		point = 0;

		while (1){
			if (q + Hog.CellX > Hog.BlockX){
				q = 0;
				p += Hog.CellY;
			}
			if(p + Hog.CellY > Hog.BlockY)		break;
			//printf("%d %d %d %d \n", i, j, p, q);
			memset(Histogram, 0, sizeof(Histogram));
			BlockSum = 0;
			
			//Statistic histogram
			for (m = 0; m < Hog.CellY; m ++){
				for(n = 0; n < Hog.CellX; n ++){
					Val = Gradient[(i + p + m) * Hog.width + j + q + n];
					Ang = Angle[(i + p + m) * Hog.width + j + q + n];
					
					Local = 0;
					while (1){
						if (Ang < 0)			Ang += 180;
						else if(Ang >= 180)		Ang -= 180;
						else					break;
					}
					//printf("%f  ", Ang);
					Local = (int)Ang / Step;
					Histogram[Local] += Val;
					BlockSum += Val;
				}
			}
			
			if (BlockSum == 0) 					BlockSum = 1;
			//Normalization
			for (r = 0; r < Hog.nbins; r ++){
				Histogram[r] /= BlockSum;
			}
			//write into result
			
			memcpy(HogResult + Hog.BlockLength * (ttl - 1) + point * Hog.nbins , Histogram, sizeof(Histogram));
			point ++;
			q += Hog.CellX;
		}

		j += Hog.StrideX;
	}

	return ;
}
