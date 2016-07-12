PYTHON_FLAGS := $(shell python-config --cflags --libs)
SDL_FLAGS := $(shell sdl2-config --cflags --libs) -lSDL2_mixer
OPENGL_FLAGS := -framework OpenGL
CORE_FLAGS := $(SDL_FLAGS) $(OPENGL_FLAGS)
