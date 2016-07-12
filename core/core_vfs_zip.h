#include "core_common.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "junzip.h"

struct ListFilesContext {
    const char *prefix;
    const char *dirname;
    int dirname_len;
    int used;
    int size;
    char **result;
};

int
ListFilesContext_recordCallback(JZFile *zip, int idx, JZFileHeader *header, char *filename, void *user_data)
{
    struct ListFilesContext *ctx = user_data;

    int filename_len = (int)strlen(filename);

    if (strstr(filename, ctx->dirname) == filename && filename_len > ctx->dirname_len + 1 && filename[ctx->dirname_len] == '/') {
        if (ctx->used == ctx->size) {
            ctx->size += ctx->size;
            ctx->result = realloc(ctx->result, sizeof(char *) * ctx->size);
        }

        asprintf(&ctx->result[ctx->used++], "%s/%s", ctx->prefix, filename + ctx->dirname_len + 1);
    }

    return 1;
}

static void
iterate_zipfile(const char *filename, JZRecordCallback callback, void *user_data)
{
    FILE *fp = fopen(filename, "rb");

    if (!fp) {
        return;
    }

    JZFile *zip = jzfile_from_stdio_file(fp);

    if (!zip) {
        return;
    }

    JZEndRecord endRecord;
    if (jzReadEndRecord(zip, &endRecord)) {
        zip->close(zip);
    }

    jzReadCentralDirectory(zip, &endRecord, callback, user_data);

    zip->close(zip);
}

static char **
list_files_zip(const char *zipfile, const char *dirname, int *count)
{
    struct ListFilesContext ctx;
    ctx.prefix = dirname;
    ctx.dirname = resolve_file_path(dirname);
    ctx.dirname_len = (int)strlen(ctx.dirname);
    ctx.used = 0;
    ctx.size = 16;
    ctx.result = malloc(sizeof(char *) * ctx.size);

    iterate_zipfile(zipfile, ListFilesContext_recordCallback, &ctx);

    *count = ctx.used;
    return ctx.result;
}

struct ReadFileContext {
    char *filename;
    int len;
    char *buf;
};

int
ReadFileContext_recordCallback(JZFile *zip, int idx, JZFileHeader *header, char *filename, void *user_data)
{
    struct ReadFileContext *ctx = user_data;

    if (strcmp(filename, ctx->filename) == 0) {
        long offset = zip->tell(zip);

        zip->seek(zip, header->offset, SEEK_SET);

        JZFileHeader header;
        jzReadLocalFileHeader(zip, &header, NULL, 0);

        ctx->len = header.uncompressedSize;
        ctx->buf = malloc(ctx->len);
        jzReadData(zip, &header, ctx->buf);

        zip->seek(zip, offset, SEEK_SET);

        return 0;
    }

    return 1;
}

static char *
read_file_zip(const char *zipfile, const char *filename, int *length)
{
    struct ReadFileContext ctx;
    ctx.filename = resolve_file_path(filename);
    ctx.len = 0;
    ctx.buf = NULL;

    iterate_zipfile(zipfile, ReadFileContext_recordCallback, &ctx);

    free(ctx.filename);

    *length = ctx.len;
    return ctx.buf;
}
