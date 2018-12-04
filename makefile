InpFolder="Input/rgbDay"
TestFolder="Input/Test"

CXX ?= g++
CFLAGS = -Wall -Wconversion -O3 -fPIC
SHVER = 2
OS = $(shell uname)

main: main.c svm.o
	gcc $(CFLAGS) -I ./lib main.c svm.o -o main -lm

svm.o: lib/svm.cpp lib/svm.h
	$(CXX) $(CFLAGS) -c lib/svm.cpp 

mark:
	@ipython Main.py train ${InpFolder}
	@rm -rf Output/Img1.png
	@rm -rf Output/Img2.png
	@rm -rf DiffImg.dat
	@rm -rf HogDEMOResult.dat
	@rm -rf ClusterImg.dat

train:
	@ipython Main.py trainff Output/SaveTrain.dat

test:
	@rm -rf tmpout
	@mkdir tmpout
	@ipython Main.py test ${TestFolder} 

clean:
	@rm -rf ./main
	@rm -rf ./mainpy
	@rm -rf CARLA.log
	@rm -rf Output/
	@rm -rf tmpout
	
	@mkdir Output/
	@mkdir Output/WARNING
	@mkdir tmpout













