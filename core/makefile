SDL_FLAGS := $(shell sdl-config --cflags --libs) -lSDL_mixer
PYTHON_FLAGS := $(shell /usr/bin/python-config --cflags --libs)
OPENGL_FLAGS := -framework OpenGL
SHLIB_FLAGS := -shared -fPIC

FLAGS := $(SDL_FLAGS) $(PYTHON_FLAGS) $(OPENGL_FLAGS) $(SHLIB_FLAGS)

all:
	gcc $(FLAGS) -o core.so core.c
