/*=================================================================
//
//		ESC project
//		ImageIO.h
//		Copyright(c) by Kazuki Amakawa, all right reserved
//
=================================================================*/

#ifndef IMAGEIOInit
#define IMAGEIOInit
unsigned char *ReadFromFile(char *FileName, unsigned char *img, int *Oheight, int *Owidth)
{
	/*
	This function will read image from file, it will save image as unsigned char
	If you want to work this algorithm from other function directly, DO NOT USE IT
	*/
	int i, j;
	FILE *File;
	File = fopen(FileName, "r");
	
	int tmp, width, height;
	fscanf(File, "%d%d%d", &tmp, &height, &width);
	//printf("%d  %d\n", height, width);
	img = (unsigned char *) malloc(width * height);
	*Owidth = width;
	*Oheight = height;
	
	for (i = 0; i < width; i ++){
		char tmpchar;
		for(j = 0; j < height; j ++){
			float tmp;
			fscanf(File, "%f", &tmp);
			img[i * height + j] = (unsigned char)tmp;

		}
	}
	return img;
}



void WriteToFile(char *FileName, unsigned char *img, int height, int width){
	#ifdef DEBUG
		printf("%s\n", FileName);
	#endif
	int i, j;
	FILE *File;
	File = fopen(FileName, "wb");
	if(File != NULL)
	{	
		fprintf(File, "%d %d %d\n", 1, height, width);
		for (i = 0; i < height; i ++){
			for (j = 0; j < width; j ++){

				fprintf(File, "%d ", (int)img[i * width + j]);
			}
			fprintf(File, "\n");
		}
		fclose(File);
		File = NULL;
	}
	return ;
}




void FloatWriteToFile(char *FileName, float *img, int height, int width){
	#ifdef DEBUG
		printf("%s\n", FileName);
	#endif
	int i, j;
	FILE *File;
	File = fopen(FileName, "wb");
	if(File != NULL)
	{
		fprintf(File, "%d %d %d\n", 1, height, width);
		for (i = 0; i < height; i ++){
			for (j = 0; j < width; j ++){
				fprintf(File, "%f ", img[i * width + j]);
			}
			fprintf(File, "\n");
		}
		fclose(File);
		File = NULL;
	}
	return ;
}



void Write2D(char *FileName, int height, int width, int img[height][width]){
	#ifdef DEBUG
		printf("%s\n", FileName);
	#endif
	int i, j;
	FILE *File;
	File = fopen(FileName, "wb");
	if(File != NULL)
	{
		fprintf(File, "%d %d %d\n", 1, height, width);
		for (i = 0; i < height; i ++){
			for (j = 0; j < width; j ++){
				//printf("%d  %d  %d  \n", i, j, img[i][j]);
				fprintf(File, "%d ", img[i][j]);
			}
			fprintf(File, "\n");
		}
		fclose(File);
		File = NULL;
	}
	return ;
}
#endif



