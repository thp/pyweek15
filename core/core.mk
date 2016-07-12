PYTHON_FLAGS := $(shell python-config --cflags --libs)
SDL_FLAGS := $(shell sdl-config --cflags --libs) -lSDL_mixer
OPENGL_FLAGS := -framework OpenGL
CORE_FLAGS := $(SDL_FLAGS) $(OPENGL_FLAGS)
