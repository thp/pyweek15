#include "core_common.h"

#include <stdio.h>
#include <stdlib.h>
#include <dirent.h>

static char *
resolve_file_path(const char *filename)
{
    char *result;
    asprintf(&result, "sdmc:/onewhaletrip/data/%s", filename);
    return result;
}

static char **
list_files(const char *dirname, int *count)
{
    char *path = resolve_file_path(dirname);
    DIR *dir = opendir(path);
    free(path);

    int used = 0;
    int size = 16;

    char **result = malloc(sizeof(char *) * size);

    struct dirent *ent;
    while ((ent = readdir(dir)) != NULL) {
        if (strcmp(ent->d_name, ".") == 0 || strcmp(ent->d_name, "..") == 0) {
            continue;
        }

        if (used == size) {
            size += size;
            result = realloc(result, sizeof(char *) * size);
        }

        asprintf(&result[used++], "%s/%s", dirname, ent->d_name);
    }

    closedir(dir);

    *count = used;
    return result;
}

static void
list_files_free(char **result, int count)
{
    for (int i=0; i<count; i++) {
        free(result[i]);
    }
    free(result);
}

static char *
read_file(const char *filename, int *length)
{
    char *path = resolve_file_path(filename);
    FILE *fp = fopen(path, "rb");
    free(path);

    fseek(fp, 0, SEEK_END);
    int len = (int)ftell(fp);

    char *buf = malloc(len);
    fseek(fp, 0, SEEK_SET);
    fread(buf, len, 1, fp);

    fclose(fp);

    *length = len;
    return buf;
}
