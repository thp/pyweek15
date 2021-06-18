PYTHON_FLAGS := $(shell python3-config --cflags --ldflags --libs --embed)
SDL_FLAGS := $(shell sdl2-config --cflags --libs) -lSDL2_mixer
ifeq ($(uname),Darwin)
OPENGL_FLAGS := -framework OpenGL
else
OPENGL_FLAGS := -lGL
endif
CORE_FLAGS := $(SDL_FLAGS) $(OPENGL_FLAGS)
