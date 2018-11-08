main:
	@gcc -I ./lib ./main.c -o main
	@./main
	@rm -rf ./main

train:
	@ipython SVMTrain.py

sign:
	@ipython Sign.py

clean:
	rm -rf ./HogMain
	rm -rf ./Hog
	rm -rf ./main
