PYTHON_BUILD := Python-2.7.12

all: onewhaletrip

Python-2.7.12.tar.xz:
	wget https://www.python.org/ftp/python/2.7.12/Python-2.7.12.tar.xz

$(PYTHON_BUILD)/libpython2.7.a: Python-2.7.12.tar.xz
	tar xvf Python-2.7.12.tar.xz
	cp ../core/core.c Setup.dist $(PYTHON_BUILD)/Modules/
	(cd Python-2.7.12 && ./configure --without-doc-strings --without-threads --disable-shared)
	$(MAKE) -C $(PYTHON_BUILD) Parser/pgen Include/graminit.h libpython2.7.a python.exe

onewhaletrip: $(PYTHON_BUILD)/libpython2.7.a
	gcc -o $@ main.c $(PYTHON_BUILD)/libpython2.7.a -I$(PYTHON_BUILD)/Include -I$(PYTHON_BUILD) \
	    -lSDL -lSDLmain -lSDL_mixer -framework OpenGL -Wl,-framework,Cocoa -lz \
	    -L/usr/local/lib -I/usr/local/include/SDL \
	    -I../core
	strip $@
	upx $@
	(cd .. && zip -r standalone/packed data engine/*.py)
	cat packed.zip >>$@

clean:
	rm -f onewhaletrip packed.zip

distclean: clean
	rm -rf $(PYTHON_BUILD)
