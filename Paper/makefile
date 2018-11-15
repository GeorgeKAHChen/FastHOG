filename = Presentation

main:
	xelatex ${filename}.tex
	#bibtex ${filename}.aux
	#xelatex ${filename}.tex
	xelatex ${filename}.tex
	rm -rf ${filename}.{ps,log,aux,out,dvi,bbl,blg,thm,toc,nav,snm}


clean:
	rm -rf ${filename}.pdf
	rm -rf ${filename}.{ps,log,aux,out,dvi,bbl,blg,thm,toc,nav,snm}
