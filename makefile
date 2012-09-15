
PACKAGE := onewhaletrip

DESTDIR ?=

all:
	@echo "nothing to be done."

convert:
	convert assets/whale_a_1.png -resize 150x150 data/sprites/whale_a-1.png
	convert assets/whale_a_2.png -resize 150x150 data/sprites/whale_a-2.png
	convert assets/whale_a_3.png -resize 150x150 data/sprites/whale_a-3.png
	convert assets/whale_b_1.png -resize 150x150 data/sprites/whale_b-1.png
	convert assets/whale_b_2.png -resize 150x150 data/sprites/whale_b-2.png
	convert assets/whale_b_3.png -resize 150x150 data/sprites/whale_b-3.png
	convert assets/whale_c_1.png -resize 150x150 data/sprites/whale_c-1.png
	convert assets/whale_c_2.png -resize 150x150 data/sprites/whale_c-2.png
	convert assets/whale_c_3.png -resize 150x150 data/sprites/whale_c-3.png
	convert assets/lanternfish_1.png -resize 130x130 data/sprites/lanternfish-1.png
	convert assets/lanternfish_2.png -resize 130x130 data/sprites/lanternfish-2.png
	convert assets/lanternfish_3.png -resize 130x130 data/sprites/lanternfish-3.png
	convert assets/diver_1.png -resize 130x130 data/sprites/diver-1.png
	convert assets/diver_2.png -resize 130x130 data/sprites/diver-2.png
	convert assets/diver_3.png -resize 130x130 data/sprites/diver-3.png
	convert assets/fishy_rainbow_1.png -resize 130x130 data/sprites/fishy_rainbow-1.png
	convert assets/fishy_rainbow_2.png -resize 130x130 data/sprites/fishy_rainbow-2.png
	convert assets/fishy_red_1.png -resize 130x130 data/sprites/fishy_red-1.png
	convert assets/fishy_red_2.png -resize 130x130 data/sprites/fishy_red-2.png
	convert assets/fishy_deepsea_1.png -resize 130x130 data/sprites/fishy_deepsea-1.png
	convert assets/fishy_deepsea_2.png -resize 130x130 data/sprites/fishy_deepsea-2.png
	convert assets/seaweed_1.png -resize 130x130 data/sprites/seaweed-1.png
	convert assets/seaweed_2.png -resize 130x130 data/sprites/seaweed-2.png
	convert assets/oyster_0_pearl.png -resize 105x105 data/sprites/oyster_0_pearl-1.png
	convert assets/oyster_1_pearl.png -resize 105x105 data/sprites/oyster_1_pearl-1.png
	convert assets/oyster_2_pearl.png -resize 105x105 data/sprites/oyster_2_pearl-1.png
	convert assets/oyster_3_pearl.png -resize 105x105 data/sprites/oyster_3_pearl-1.png
	convert assets/shell.png -resize 100x100 data/sprites/shell-1.png
	convert assets/sandboxtoys.png -resize 98x98 data/sprites/sandboxtoys-1.png
	convert assets/pearl.png -resize 100x100 data/sprites/pearl-1.png
	cp assets/whale_ico_0.png data/sprites/whale_ico-0.png
	convert assets/whale_icon_1.png -resize 41x41 data/sprites/whale_ico-3.png
	convert assets/whale_icon_2.png -resize 41x41 data/sprites/whale_ico-2.png
	convert assets/whale_icon_3.png -resize 41x41 data/sprites/whale_ico-1.png
	convert assets/pearlcount_icon.png -resize 20x20 data/sprites/pearlcount_icon-1.png
	convert assets/levelbg_test.png -resize 800x480 data/backgrounds/test-1.jpg
	convert assets/bg_surreal_1.jpg -resize 800x480 data/backgrounds/surreal-1.jpg
	convert assets/bg_surreal_2.jpg -resize 800x480 data/backgrounds/surreal-2.jpg
	convert assets/bg_surreal_3.jpg -resize 800x480 data/backgrounds/surreal-3.jpg
	convert assets/bg_beach.jpg -resize 800x480 data/backgrounds/beach-1.jpg

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

