InpFolder="Input/TestInput"

main:
	@gcc -I ./lib ./main.c -o main
	@./main
	@rm -rf ./main

Sign:
	ipython Main.py train ${InpFolder}

train:
	@ipython Main.py trainff Output/SaveTrain.dat

test:
	@ipython Main.py test ${InpFolder}

clean:
	@rm -rf ./main
	@rm -rf ./mainpy
	@rm -rf CARLA.log
	@rm -rf Output/

	@mkdir Output/
	@mkdir Output/WARNING