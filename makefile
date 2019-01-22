InpFolder="Input/rgbDay"
TestFolder="Input/Test"

CXX ?= g++
CFLAGS = -Wall -Wconversion -O3 -fPIC
OS = $(shell uname)


main: libsvm.so
	gcc main.c -o main -L. -lsvm -Wl,-rpath,./
	gcc svm-train.c -o train -L./ -lsvm -Wl,-rpath,./
#gcc -o main -L. –ltest -Wl,-rpath=/root/test/lib test.c

libsvm.so:
	$(CXX) $(CFLAGS) -c svm.cpp 
	if [ "$(OS)" = "Darwin" ]; then \
		SHARED_LIB_FLAG="-dynamiclib -Wl,-install_name,libsvm.so.$(SHVER)"; \
	else \
		SHARED_LIB_FLAG="-shared -Wl,-soname,libsvm.so.$(SHVER)"; \
	fi; \
	$(CXX) $${SHARED_LIB_FLAG} svm.o -o libsvm.so

test:
	./train

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













