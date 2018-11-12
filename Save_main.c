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
#include <HogPixel.h>
#include <time.h>

#define DEBUG
#define DEMO

int main(int argc, char const *argv[])
{
/*============================================================
Parameter
*/
	int epision = 4;
	int minS = 25;
	int NegativeVal = 10;
	int Oheight = 288;
	int Owidth = 512;
	int height = 32;
	int width = 18;
	float DetectProb = 0.5;


/*============================================================
Variable Definition
*/
	unsigned char *img1;
	unsigned char *img2;
	int i, j, p, q, ValX, ValY;
	int ClusImg[Oheight][Owidth];
	unsigned char *PartialImg;
	clock_t StartTime, EndTime, TotalStart, TotalEnd;



/*============================================================
Algorithm: Initialization
*/
	img1 = ReadFromFile("Input/Inp1.dat", img1, &Oheight, &Owidth);

	DBSCANInit(epision, Oheight, Owidth);		//Initial DBSCAN
	Hog.width = width;
	Hog.height = height;
	HogInit();									//Initial HOG
	
	PartialImg = (unsigned char *) malloc(width * height * sizeof(unsigned char));



/*============================================================
Algortihm: Differential Images
*/
	img2 = ReadFromFile("Input/Inp2.dat", img2, &Oheight, &Owidth);

#ifdef DEBUG	
	TotalStart = clock();
	StartTime = clock();
#endif

	int DiffImg[Oheight][Owidth];
	for (i = 0; i < Oheight; i ++){
		for (j = 0; j < Owidth; j ++){
			if ((int)img1[i * Owidth + j] - (int)img2[i * Owidth + j] > NegativeVal || 
				(int)img1[i * Owidth + j] - (int)img2[i * Owidth + j] < -NegativeVal )
												DiffImg[i][j] = 1;
			else								DiffImg[i][j] = 0;
		}
	}

#ifdef DEBUG
	EndTime = clock();
	printf("Differential: %f\n", (double)(EndTime - StartTime)/ CLOCKS_PER_SEC);
	//Write2D("tmpout/tmp.dat", Oheight, Owidth, DiffImg);
#endif
	


/*============================================================
Algorithm: DBSCAN Part
*/
#ifdef DEBUG
	StartTime = clock();
#endif
	memset(ClusImg, 0, sizeof(ClusImg));
	//printf("%d  %d\n", Oheight, Owidth);
	DBSCAN(Oheight, Owidth, DiffImg, minS, ClusImg);

#ifdef DEBUG
	//printf("ClusterVal: %d\n", ClusterVal);
	EndTime = clock();
	printf("Cluster: %f\n", (double)(EndTime - StartTime)/ CLOCKS_PER_SEC);
	Write2D("tmpout/tmp.dat", Oheight, Owidth, ClusImg);
#endif	
	


/*============================================================
Algorithm: HOG Part
*/
#ifdef DEBUG
	StartTime = clock();
#endif

#ifdef DEMO	
	FILE *File;
	File = fopen("Output/HogDEMOResult.dat", "wb");
#endif

	for (i = 0; i < TotalOutNode; i ++){
		if (ClusImg[OuterNode[2 * i]] [OuterNode[2 * i + 1]] <= 0)
			continue;
		for (p = -height/2; p < (height+1)/2; p ++){
			for (q = -width/2; q < (width+1)/2; q ++){
				ValY = OuterNode[  2 * i  ] + p;
				ValX = OuterNode[2 * i + 1] + q;
				if (ValY < 0 || ValY >= Oheight || ValX < 0 || ValX >= Owidth)
												PartialImg[(p + height/2) * width + q + width/2] = (unsigned char)0;
				else							PartialImg[(p + height/2) * width + q + width/2] = img2[ValY * Oheight + ValX];
			}
		}
		//WriteToFile("tmpout/tmp1.dat", PartialImg, Hog.height, Hog.width)
		GetImage(PartialImg);
		HogImg();

#ifdef DEMO
		if(File != NULL)
		{
			fprintf(File, "%d %d %d ", ClusImg[OuterNode[2 * i]] [OuterNode[2 * i + 1]], OuterNode[2 * i], OuterNode[2 * i + 1]);
			for (j = 0; j < Hog.nbins; j ++){
				fprintf(File, "%f ", HogResult[j]);
			}
			fprintf(File, "\n");
		}
#endif

	}
	


/*============================================================
Algorithm: SVM Classificatin
*/





/*============================================================
Algorithm: Probability Decision
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
*/
	//FloatWriteToFile("Output/Result.dat", HogResult,  Hog.height * Hog.width, Hog.nbins);

	
	return 0;
}