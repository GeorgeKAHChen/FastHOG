InpFolder="Input/PRWTrain/Group1"
TestFolder="Input/Test"

main:
	@gcc -I ./lib ./main.c -o main
	@./main
	@rm -rf ./main

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
