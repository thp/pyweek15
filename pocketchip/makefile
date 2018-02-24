TARGET := onewhaletrip
TARGET_SRC := main.c core/core.c core/junzip.c eglo/eglo.cpp

PYTHON_FLAGS := $(shell python3-config --cflags --ldflags --libs)
SDL_FLAGS := $(shell sdl2-config --cflags --libs) -lSDL2_mixer
OPENGL_FLAGS := -lGLESv2 -lEGL -lX11 -lz
CORE_FLAGS := -Wno-missing-braces -Icore -Ieglo $(SDL_FLAGS) $(PYTHON_FLAGS) $(OPENGL_FLAGS)

all: $(TARGET)

%.o: %.c
	gcc -c -o $@ $< $(CORE_FLAGS) -std=c11

%.o: %.cpp
	g++ -c -o $@ $< $(CORE_FLAGS) -std=c++11

$(TARGET): $(patsubst %.cpp,%.o,$(patsubst %.c,%.o,$(TARGET_SRC)))
	g++ -o $@ $^ $(CORE_FLAGS) -std=c++11
	strip -s $@
	rm -f $(TARGET).zip
	(cd .. && zip -9 -r pocketchip/$(TARGET) data engine/*.py)
	cat $(TARGET).zip >>$@
	rm -f $(TARGET).zip

DEB := onewhaletrip.deb

deb: $(DEB)

$(DEB): $(TARGET)
	rm -rf tmp data.tar.gz control.tar.gz control debian-binary $(DEB)
	mkdir -p tmp/usr/bin
	cp $(TARGET) tmp/usr/bin/onewhaletrip
	tar cJvf data.tar.xz -C tmp usr
	sed -e "s/--SIZE--/`du -sk tmp | awk '{ print $$1 }'`/" control.in > control
	tar cJvf control.tar.xz control
	echo 2.0 > debian-binary
	ar r $(DEB) debian-binary control.tar.xz data.tar.xz
	rm -rf debian-binary control.tar.xz data.tar.xz control tmp

clean:
	rm -f $(TARGET) $(TARGET).zip

distclean: clean
	rm -rf $(PYTHON_BUILD) $(PYTHON_SOURCE)

.PHONY: all clean distclean deb
