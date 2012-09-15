
PACKAGE := onewhaletrip

DESTDIR ?=

all:
	@echo "nothing to be done."

convert:
	python convert_sprites.py

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

