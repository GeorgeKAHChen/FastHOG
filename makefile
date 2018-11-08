InpFloder="Input/TestInput"

main:
	@gcc -I ./lib ./main.c -o main
	@./main
	@rm -rf ./main

train:
	@ipython Main.py train ${InpFloder}

test:
	@ipython Main.py test ${InpFloder}

clean:
	@rm -rf ./main

cleanall:
	@rm -rf ./main
	@rm -rf CARLA.log
	@rm -rf Output/

	@mkdir Output/