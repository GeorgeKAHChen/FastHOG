InpFolder="Input/rgbDay"
TestFolder="Input/Test"

CXX ?= g++
CFLAGS = -Wall -Wconversion -O3 -fPIC
OS = $(shell uname)


main: lib
	gcc main.c -L. -lsvm -o main
	gcc svm-train.c -L. -lsvm -o train

lib: svm.o
	if [ "$(OS)" = "Darwin" ]; then \
		SHARED_LIB_FLAG="-dynamiclib -Wl,-install_name,libsvm.so"; \
	else \
		SHARED_LIB_FLAG="-shared -Wl,-soname,libsvm.so"; \
	fi; \
	$(CXX) $${SHARED_LIB_FLAG} svm.o -o libsvm.so
	

svm.o: svm.cpp svm.h
	$(CXX) $(CFLAGS) -c svm.cpp 

test:
	./main

mark:
	@ipython Main.py train ${InpFolder}
	@rm -rf Output/Img1.png
	@rm -rf Output/Img2.png
	@rm -rf DiffImg.dat
	@rm -rf HogDEMOResult.dat
	@rm -rf ClusterImg.dat

train: libsvm.so
	@ipython Main.py trainff Output/SaveTrain.dat

clean:
	@rm -rf ./main ./train CARLA.log Output/ tmpout
	@rm -f *~ svm.o svm-train svm-predict svm-scale libsvm.so
	@mkdir Output/
	@mkdir Output/WARNING
	@mkdir tmpout

