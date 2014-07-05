OS = $(shell uname -s)
TOOL =
TO_REMOVE = 

ifeq ("$(OS)","Linux")
	TOOL = texi2pdf
	TO_REMOVE = *.out *.log *.aux
else 
	ifeq ("$(OS)","Darwin")
		TOOL = pdflatex
	endif
endif

all:
	$(TOOL) Hotkeys.tex
	$(TOOL) CmdLineOptions.tex
	$(TOOL) marioai-lvlgen-options-usage.tex
	rm $(TO_REMOVE)
	mv *.pdf ../
