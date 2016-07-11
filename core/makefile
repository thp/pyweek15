include core.mk

all:
	gcc -shared -fPIC $(CORE_FLAGS) $(PYTHON_FLAGS) -o core.so core.c

clean:
	rm -rf core.so core.so.dSYM
