
PACKAGE := onewhaletrip

DESTDIR ?=

all:
	@echo "nothing to be done."

convert:
	convert assets/whale_a_1.png -resize 100x100 data/sprites/whale_a_1.png
	convert assets/whale_a_2.png -resize 100x100 data/sprites/whale_a_2.png
	convert assets/whale_a_2.png -resize 100x100 data/sprites/whale_a_3.png
	convert assets/levelbg_test.png -resize 800x480 data/sprites/bg.png

install:
	mkdir -p $(DESTDIR)/opt/$(PACKAGE)/bin
	install -m755 $(PACKAGE) $(DESTDIR)/opt/$(PACKAGE)/bin/
	cp -rpv data $(DESTDIR)/opt/$(PACKAGE)/
	cp -rpv src $(DESTDIR)/opt/$(PACKAGE)/
	cp -rpv docopt.py $(DESTDIR)/opt/$(PACKAGE)/src/
	install -D $(PACKAGE).desktop $(DESTDIR)/usr/share/applications/$(PACKAGE).desktop
	install -D $(PACKAGE).png $(DESTDIR)/opt/$(PACKAGE)/$(PACKAGE).png

clean:
	find . -name '*.pyc' -exec rm '{}' +

.PHONY: all convert install clean
.DEFAULT: all

