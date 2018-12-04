#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include "svm.h"

#ifndef SVMPredict
#define SVMPredict


int print_null(const char *s,...) {return 0;}

struct svm_node *x;
struct svm_model* model;



void exit_input_error(int line_num)
{
	fprintf(stderr,"Wrong input format at line %d\n", line_num);
	exit(1);
}



int svm_Initial(int SizeofVector, char *ModelFileName){
	x = (struct svm_node *) malloc(SizeofVector * sizeof(struct svm_node));

	if((model=svm_load_model(ModelFileName))==0)
	{
		fprintf(stderr,"can't open model file %s\n", ModelFileName);
		exit(1);
	}

	if(svm_check_probability_model(model)!=0)
		printf("Model supports probability estimates, but disabled in prediction.\n");

}



double read_from_memory(int DataSize, float *Data){
	int i, j;
	double predict_label;

	for (i = 0; i < DataSize; i ++){
		x[i].index = i + 1;
		x[i].value = Data[i];
	}
	x[i].index = -1;

	predict_label = svm_predict(model,x);
	
	return predict_label;
}


#endif




