main:
	@gcc -I ./lib ./DBSCANMain.c -o DBSCANMain -v
	@./DBSCANMain

train:
	@python SVMTrain.py

sign:
	@python Sign.py

clean:
	rm -rf ./HogMain
	rm -rf ./Hog
