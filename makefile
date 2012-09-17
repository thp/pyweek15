
PACKAGE := onewhaletrip

DESTDIR ?=

all:
	@echo "nothing to be done."

convert:
	python convert_sprites.py

crunch-files:
	# Make files smaller for distribution
	# (don't commit the changes, though - use "undo-crunch")
	(cd data/sprites/ && pngnq *.png)
	(cd data/sprites/ && for file in *-nq8.png; do mv $$file $$(basename $$file -nq8.png).png; done)
	(cd data/creatures/ && pngnq *.png)
	(cd data/creatures/ && for file in *-nq8.png; do mv $$file $$(basename $$file -nq8.png).png; done)
	(cd data/backgrounds/ && for file in *.jpg; do convert $$file -quality 70 $$file; done)
	(cd data/sounds/ && oggenc -q0 *.wav && rm *.wav)


undo-crunch:
	# Undo "crunch-files" (after distribution package is built)
	find data -name '*.orig' -exec rm '{}' +
	hg revert data
	rm -f data/sounds/*.ogg

install:
	mkdir -p $(DESTDIR)/opt/$(PACKAGE)/bin
	install -m755 $(PACKAGE) $(DESTDIR)/opt/$(PACKAGE)/bin/
	cp -rpv data $(DESTDIR)/opt/$(PACKAGE)/
	cp -rpv src $(DESTDIR)/opt/$(PACKAGE)/
	cp -rpv docopt.py gles1.py $(DESTDIR)/opt/$(PACKAGE)/src/
	install -D $(PACKAGE).desktop $(DESTDIR)/usr/share/applications/$(PACKAGE).desktop
	install -D $(PACKAGE).png $(DESTDIR)/opt/$(PACKAGE)/$(PACKAGE).png

clean:
	find . -name '*.pyc' -exec rm '{}' +

.PHONY: all convert crunch-files undo-crunch install clean
.DEFAULT: all

