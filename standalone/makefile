TARGET := onewhaletrip
TARGET_SRC := main.c ../core/core.c ../core/junzip.c

PYTHON_MAJOR := 2.7
PYTHON_VERSION := 2.7.12

PYTHON_BUILD := Python-$(PYTHON_VERSION)
PYTHON_SOURCE := $(PYTHON_BUILD).tar.xz
PYTHON_FLAGS := -I$(PYTHON_BUILD)/Include -I$(PYTHON_BUILD) -lz

PYTHON_STATIC := $(PYTHON_BUILD)/libpython$(PYTHON_MAJOR).a

SDL2_BUILD := sdl2-install
SDL2_CONFIG := $(SDL2_BUILD)/bin/sdl2-config
SDL_FLAGS := `$(SDL2_CONFIG) --cflags --libs`

SDL2_STATIC := $(SDL2_BUILD)/lib/libSDL2.a
SDL2_MIXER_STATIC := $(SDL2_BUILD)/lib/libSDL2_mixer.a

OPENGL_FLAGS := -framework OpenGL
CORE_FLAGS := $(SDL_FLAGS) $(OPENGL_FLAGS) $(PYTHON_FLAGS)

all: $(TARGET)

$(PYTHON_SOURCE):
	wget https://www.python.org/ftp/python/$(PYTHON_VERSION)/$(PYTHON_SOURCE)

$(PYTHON_STATIC): $(PYTHON_SOURCE)
	rm -rf $(YPTHON_BUILD)
	tar xvf $(PYTHON_SOURCE)
	cp Setup.dist $(PYTHON_BUILD)/Modules/
	(cd $(PYTHON_BUILD) && ./configure --without-doc-strings --without-threads --disable-shared)
	$(MAKE) -C $(dir $@) $(notdir $@)

$(SDL2_STATIC):
	sh build_sdl2.sh

$(TARGET): $(TARGET_SRC) $(PYTHON_STATIC) $(SDL2_STATIC) $(SDL2_MIXER_STATIC)
	gcc -o $@ $^ $(CORE_FLAGS) -I../core
	strip $@
	upx $@
	rm -f $(TARGET).zip
	(cd .. && zip -r standalone/$(TARGET) data engine/*.py)
	cat $(TARGET).zip >>$@
	rm -f $(TARGET).zip

osx-bundle: $(TARGET)
	mkdir -p "One Whale Trip.app/Contents/MacOS" "One Whale Trip.app/Contents/Resources"
	cp ../assets/icon.icns "One Whale Trip.app/Contents/Resources/OneWhaleTrip.icns"
	cp $(TARGET) "One Whale Trip.app/Contents/MacOS/OneWhaleTrip"
	cp ../assets/Info.plist "One Whale Trip.app/Contents"

clean:
	rm -f $(TARGET) $(TARGET).zip

distclean: clean
	rm -rf $(PYTHON_BUILD) $(PYTHON_SOURCE)

.PHONY: all osx-bundle clean distclean
