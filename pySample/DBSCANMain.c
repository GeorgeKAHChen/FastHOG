#include <stdio.h>
#include <string.h>
#include <DBSCAN.h>
#include <ImageIO.h>

#include <time.h>

int main(int argc, char const *argv[])
{
	int epision = 4;
	int minS = 25;

	int i, j;
	int Oheight, Owidth;
	unsigned char *img;
	
	img = ReadFromFile("Input/Inp1.dat", img, &Oheight, &Owidth);
	int DiffImg[Oheight][Owidth];
	memset(DiffImg, 0, sizeof(DiffImg));
	for (i = 0; i < Oheight; i ++){
		for (j = 0; j < Owidth; j ++){
			if ((int)img[i * Owidth + j] != 0)	{
				DiffImg[i][j] = 1;
			}
		}
	}

	DBSCANInit(4, 144, 256);

	int ResImg[Oheight][Owidth];
	clock_t StartTime, EndTime;

	StartTime = clock();
	memset(ResImg, 0, sizeof(ResImg));
	DBSCAN(Oheight, Owidth, DiffImg, minS, ResImg);
	EndTime = clock();
	printf("%f\n", (double)(EndTime - StartTime)/ CLOCKS_PER_SEC);
	
	Write2D("tmp.dat", Oheight, Owidth, ResImg);
	printf("ClusterVal: %d\n", ClusterVal);
	

	return 0;
}