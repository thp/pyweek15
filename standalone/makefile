include ../core/core.mk

PYTHON_MAJOR := 2.7
PYTHON_VERSION := 2.7.12

PYTHON_BUILD := Python-$(PYTHON_VERSION)
PYTHON_SOURCE := $(PYTHON_BUILD).tar.xz
PYTHON_STATIC := $(PYTHON_BUILD)/libpython$(PYTHON_MAJOR).a
PYTHON_FLAGS := $(PYTHON_STATIC) -I$(PYTHON_BUILD)/Include -I$(PYTHON_BUILD) -lz

all: onewhaletrip

$(PYTHON_SOURCE):
	wget https://www.python.org/ftp/python/$(PYTHON_VERSION)/$(PYTHON_SOURCE)

$(PYTHON_STATIC): $(PYTHON_SOURCE)
	tar xvf $(PYTHON_SOURCE)
	cp Setup.dist $(PYTHON_BUILD)/Modules/
	(cd $(PYTHON_BUILD) && ./configure --without-doc-strings --without-threads --disable-shared)
	$(MAKE) -C $(PYTHON_BUILD) Parser/pgen Include/graminit.h libpython$(PYTHON_MAJOR).a python.exe

onewhaletrip: $(PYTHON_STATIC)
	gcc -o $@ main.c ../core/core.c $(PYTHON_FLAGS) $(CORE_FLAGS) -I../core
	strip $@
	upx $@
	(cd .. && zip -r standalone/onewhaletrip data engine/*.py)

clean:
	rm -f onewhaletrip onewhaletrip.zip

distclean: clean
	rm -rf $(PYTHON_BUILD)
