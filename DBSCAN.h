/*=================================================================
//
//		Fast Hog project
//		DBSCAN.h
//		Copyright(c) by Kazuki Amakawa, all right reserved
//
=================================================================*/

#ifndef DBSCANINIT
#define DBSCANINIT
int *DBSCANTable;
int SizeOfTable = 0;

int ClusterVal;
int WidthImg;

void DBSCANInit(int episilon, int height, int width);
int *DBSCAN(int height, int width, int InpImg[height][width], int minS, int LabelImg[height][width]);
#endif


void DBSCANInit(int episilon, int height, int width){
	int AreaTable[2 * episilon + 1][2 * episilon + 1];
	int i, j, Val;

	WidthImg = width;
	for (i = 0; i < 2 * episilon + 1; i ++){
		for (j = 0; j < 2 * episilon + 1; j ++){
			if (i == episilon && j == episilon)
									continue;

			if (sqrt(pow(i - episilon, 2) + pow(j - episilon, 2)) <= episilon){
				SizeOfTable ++;
				AreaTable[i][j] = 1;
			}
		}
	}

	DBSCANTable = (int *)malloc(2 * SizeOfTable * sizeof(int));
	Val = 0;

	for (i = 0; i < 2 * episilon + 1; i ++){
		for (j = 0; j < 2 * episilon + 1; j ++){
			if (AreaTable[i][j] == 1){
				DBSCANTable[  2 * Val  ] = i - episilon;
				DBSCANTable[2 * Val + 1] = j - episilon;
				Val += 1;
			}
		}
	}

	return ;
}





int *DBSCAN(int height, int width, int InpImg[height][width], int minS, int (*LabelImg)[WidthImg]){
	int i, j, k, Point, Inner, willCluster, ValY, ValX, iNew, jNew, l, noStack;
	int StackVal = 0;

	ClusterVal = 0;

	int (*Stack)[2];
	Stack = (int (*)[2]) malloc ((height * width / 20 * 2 + 50) * sizeof(int));
	

	for (i = 0; i < height; i ++){
		for (j = 0; j < width; j ++){
			//printf("%d  %d\n", i, j);
			if (InpImg[i][j] == 0)		continue;
			if (LabelImg[i][j] != 0)	continue;

			/*
			Classify Inner/Outer
			*/
			Point = 0;
			Inner = 0;
			willCluster = 0;
			
			for (k = 0; k < SizeOfTable; k ++){
				ValY = i + DBSCANTable[2 * k];
				ValX = j + DBSCANTable[2 * k + 1];
				if (ValY < 0 || ValY >= height || ValX < 0 || ValX >= width)
										continue;

				if (InpImg[ValY][ValX] == 1)
										Point ++;

				if (Point >= minS){
					Inner = 1;
					if (LabelImg[i][j] == 0){
						willCluster = 1;
						break;
					}
					else				break;

				}

			}

			/*
			Inner Cluster
			*/
			if (willCluster){
				Stack[StackVal][0] = i;
				Stack[StackVal][1] = j;
				StackVal ++;
				ClusterVal ++;
				while (1){
					StackVal --;
					iNew = Stack[StackVal][0];
					jNew = Stack[StackVal][1];
					//printf("(%d, %d)\t", iNew, jNew);
					
					LabelImg[iNew][jNew] = ClusterVal;
					for (k = 0; k < SizeOfTable; k ++){
						ValY = iNew + DBSCANTable[2 * k];
						ValX = jNew + DBSCANTable[2 * k + 1];

						if (ValY < 0 || ValY >= height || ValX < 0 || ValX >= width)
												continue;

						if (InpImg[ValY][ValX] == 0)
												continue;

						if (LabelImg[ValY][ValX] >= 1)
												continue;

						if (InpImg[ValY][ValX] == 1){
							noStack = 0;
							for (l = 0; l < StackVal; l ++){
								if (Stack[l][0] == ValY && Stack[l][1] == ValX){
									noStack = 1;
									break;
								}
								
							}
							if (noStack == 0){
								Stack[StackVal][0] = ValY;
								Stack[StackVal][1] = ValX;
								StackVal ++;
							}

						}
					}
					if (StackVal == 0)			break;

				}
			}

		}
	} 

	return LabelImg;
}