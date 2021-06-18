include core.mk

MODULE := core.so
MODULE_SRC := core.c junzip.c

CORE_FLAGS += -lz

all: $(MODULE)

$(MODULE): $(MODULE_SRC)
	$(CC) -o $@ $^ -shared -fPIC $(CORE_FLAGS) $(PYTHON_FLAGS) -Wno-missing-braces

clean:
	rm -rf $(MODULE) $(MODULE).dSYM
