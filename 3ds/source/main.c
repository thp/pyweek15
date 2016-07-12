#include "core.h"

int main()
{
    gfxInitDefault();

    consoleInit(GFX_BOTTOM, NULL);

    Py_FrozenFlag = 1;
    Py_NoSiteFlag = 1;
    Py_Initialize();

    initcore();

    PyRun_SimpleString("import sys; sys.path.insert(0, 'sdmc:/onewhaletrip'); import engine; engine.main()");

    return 0;
}
