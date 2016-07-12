include ../core/core.mk

TARGET := onewhaletrip
TARGET_SRC := main.c ../core/core.c

PYTHON_MAJOR := 2.7
PYTHON_VERSION := 2.7.12

PYTHON_BUILD := Python-$(PYTHON_VERSION)
PYTHON_SOURCE := $(PYTHON_BUILD).tar.xz
PYTHON_STATIC := $(PYTHON_BUILD)/libpython$(PYTHON_MAJOR).a
PYTHON_FLAGS := -I$(PYTHON_BUILD)/Include -I$(PYTHON_BUILD) -lz

all: $(TARGET)

$(PYTHON_SOURCE):
	wget https://www.python.org/ftp/python/$(PYTHON_VERSION)/$(PYTHON_SOURCE)

$(PYTHON_STATIC): $(PYTHON_SOURCE)
	rm -rf $(YPTHON_BUILD)
	tar xvf $(PYTHON_SOURCE)
	cp Setup.dist $(PYTHON_BUILD)/Modules/
	(cd $(PYTHON_BUILD) && ./configure --without-doc-strings --without-threads --disable-shared)
	$(MAKE) -C $(dir $@) $(notdir $@)

$(TARGET): $(TARGET_SRC) $(PYTHON_STATIC)
	gcc -o $@ $^ $(PYTHON_FLAGS) $(CORE_FLAGS) -I../core
	strip $@
	upx $@
	(cd .. && zip -r standalone/$(TARGET) data engine/*.py)

clean:
	rm -f $(TARGET) $(TARGET).zip

distclean: clean
	rm -rf $(PYTHON_BUILD) $(PYTHON_SOURCE)
