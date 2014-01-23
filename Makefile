SHELL = /bin/bash -eu
.DELETE_ON_ERROR:

README.html:

%.html: %.md
	markdown -o html4 $< > $@
	reload-tab $@ ||:
