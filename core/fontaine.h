#ifndef FONTAINE_H
#define FONTAINE_H

/**
 * Fontaine -- C89 8x8 pixel font rendering library
 * 2016-05-30 Thomas Perl <m@thp.io>
 **/

unsigned char __2048_by_oerg866_8x8s[] = {
  0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x05, 0x50, 0x07, 0xd0, 0x07,
  0xd0, 0x07, 0xd0, 0x05, 0x50, 0x07, 0xd0, 0x05, 0x50, 0x00, 0x00, 0x15,
  0x55, 0x1f, 0x7d, 0x15, 0x55, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x15, 0x55, 0x5f, 0x7d, 0x7f, 0xfd, 0x5d, 0x75, 0x7f,
  0xfd, 0x7d, 0xf5, 0x55, 0x54, 0x00, 0x00, 0x05, 0x55, 0x17, 0xfd, 0x1d,
  0xd5, 0x17, 0xf5, 0x15, 0xdd, 0x1f, 0xf5, 0x15, 0x54, 0x00, 0x00, 0x15,
  0x55, 0x1f, 0x7d, 0x15, 0x7d, 0x17, 0xf5, 0x1f, 0x55, 0x1f, 0x7d, 0x15,
  0x55, 0x00, 0x00, 0x05, 0x50, 0x17, 0xd0, 0x1d, 0x55, 0x17, 0xdd, 0x1d,
  0x75, 0x17, 0xdd, 0x05, 0x55, 0x00, 0x00, 0x05, 0x50, 0x07, 0xd0, 0x05,
  0x50, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01,
  0x54, 0x05, 0xf4, 0x07, 0xd4, 0x07, 0xd0, 0x07, 0xd4, 0x05, 0xf4, 0x01,
  0x54, 0x00, 0x00, 0x15, 0x40, 0x1f, 0x50, 0x17, 0xd0, 0x07, 0xd0, 0x17,
  0xd0, 0x1f, 0x50, 0x15, 0x40, 0x00, 0x00, 0x15, 0x55, 0x1f, 0x7d, 0x17,
  0xf5, 0x1f, 0xfd, 0x17, 0xf5, 0x1f, 0x7d, 0x15, 0x55, 0x00, 0x00, 0x01,
  0x50, 0x01, 0xd0, 0x15, 0xd5, 0x1f, 0xfd, 0x15, 0xd5, 0x01, 0xd0, 0x01,
  0x50, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x05, 0x50, 0x17,
  0xd0, 0x1f, 0x50, 0x15, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x15,
  0x55, 0x1f, 0xfd, 0x15, 0x55, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x15, 0x40, 0x1f, 0x40, 0x15,
  0x40, 0x00, 0x00, 0x00, 0x55, 0x01, 0x7d, 0x05, 0xf5, 0x17, 0xd4, 0x5f,
  0x50, 0x7d, 0x40, 0x55, 0x00, 0x00, 0x00, 0x05, 0x54, 0x17, 0xf5, 0x1f,
  0x7d, 0x1f, 0x7d, 0x1f, 0x7d, 0x17, 0xf5, 0x05, 0x54, 0x00, 0x00, 0x05,
  0x54, 0x07, 0xf4, 0x05, 0xf4, 0x01, 0xf4, 0x01, 0xf4, 0x01, 0xf4, 0x01,
  0x54, 0x00, 0x00, 0x15, 0x54, 0x1f, 0xf5, 0x15, 0x7d, 0x17, 0xf5, 0x1f,
  0x55, 0x1f, 0xfd, 0x15, 0x55, 0x00, 0x00, 0x15, 0x54, 0x1f, 0xf5, 0x15,
  0x7d, 0x07, 0xfd, 0x15, 0x7d, 0x1f, 0xf5, 0x15, 0x54, 0x00, 0x00, 0x15,
  0x55, 0x1f, 0x7d, 0x1f, 0x7d, 0x1f, 0xfd, 0x15, 0x7d, 0x00, 0x7d, 0x00,
  0x55, 0x00, 0x00, 0x15, 0x55, 0x1f, 0xfd, 0x1f, 0x55, 0x1f, 0xf5, 0x15,
  0x7d, 0x1f, 0xf5, 0x15, 0x54, 0x00, 0x00, 0x05, 0x54, 0x17, 0xf4, 0x1f,
  0x54, 0x1f, 0xf5, 0x1f, 0x7d, 0x17, 0xf5, 0x05, 0x54, 0x00, 0x00, 0x15,
  0x55, 0x1f, 0xfd, 0x15, 0x7d, 0x05, 0xf5, 0x07, 0xd4, 0x07, 0xd0, 0x05,
  0x50, 0x00, 0x00, 0x05, 0x54, 0x17, 0xf5, 0x1f, 0x7d, 0x17, 0xf5, 0x1f,
  0x7d, 0x17, 0xf5, 0x05, 0x54, 0x00, 0x00, 0x05, 0x54, 0x17, 0xf5, 0x1f,
  0x7d, 0x17, 0xfd, 0x05, 0x7d, 0x07, 0xf5, 0x05, 0x54, 0x00, 0x00, 0x00,
  0x00, 0x05, 0x50, 0x07, 0xd0, 0x05, 0x50, 0x07, 0xd0, 0x05, 0x50, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x05, 0x50, 0x07, 0xd0, 0x05, 0x50, 0x17,
  0xd0, 0x1f, 0x50, 0x15, 0x40, 0x00, 0x00, 0x01, 0x54, 0x05, 0xf4, 0x17,
  0xd4, 0x1f, 0x50, 0x17, 0xd4, 0x05, 0xf4, 0x01, 0x54, 0x00, 0x00, 0x00,
  0x00, 0x15, 0x54, 0x1f, 0xf4, 0x15, 0x54, 0x1f, 0xf4, 0x15, 0x54, 0x00,
  0x00, 0x00, 0x00, 0x15, 0x40, 0x1f, 0x50, 0x17, 0xd4, 0x05, 0xf4, 0x17,
  0xd4, 0x1f, 0x50, 0x15, 0x40, 0x00, 0x00, 0x15, 0x54, 0x1f, 0xf5, 0x15,
  0x7d, 0x07, 0xf5, 0x05, 0x54, 0x07, 0xd0, 0x05, 0x50, 0x00, 0x00, 0x15,
  0x55, 0x1f, 0xfd, 0x1d, 0x5d, 0x1d, 0xfd, 0x1d, 0x55, 0x1f, 0xfd, 0x15,
  0x55, 0x00, 0x00, 0x05, 0x54, 0x17, 0xf5, 0x1f, 0x7d, 0x1f, 0xfd, 0x1f,
  0x7d, 0x1f, 0x7d, 0x15, 0x55, 0x00, 0x00, 0x15, 0x54, 0x1f, 0xf5, 0x1f,
  0x7d, 0x1f, 0xf5, 0x1f, 0x7d, 0x1f, 0xf5, 0x15, 0x54, 0x00, 0x00, 0x05,
  0x55, 0x17, 0xfd, 0x1f, 0x55, 0x1f, 0x40, 0x1f, 0x55, 0x17, 0xfd, 0x05,
  0x55, 0x00, 0x00, 0x15, 0x54, 0x1f, 0xf5, 0x1f, 0x7d, 0x1f, 0x7d, 0x1f,
  0x7d, 0x1f, 0xf5, 0x15, 0x54, 0x00, 0x00, 0x15, 0x55, 0x1f, 0xfd, 0x1f,
  0x55, 0x1f, 0xf4, 0x1f, 0x55, 0x1f, 0xfd, 0x15, 0x55, 0x00, 0x00, 0x15,
  0x55, 0x1f, 0xfd, 0x1f, 0x55, 0x1f, 0xf4, 0x1f, 0x54, 0x1f, 0x40, 0x15,
  0x40, 0x00, 0x00, 0x05, 0x55, 0x17, 0xfd, 0x1f, 0x55, 0x1f, 0x7d, 0x1f,
  0x7d, 0x17, 0xf5, 0x05, 0x54, 0x00, 0x00, 0x15, 0x55, 0x1f, 0x7d, 0x1f,
  0x7d, 0x1f, 0xfd, 0x1f, 0x7d, 0x1f, 0x7d, 0x15, 0x55, 0x00, 0x00, 0x15,
  0x54, 0x1f, 0xf4, 0x17, 0xd4, 0x07, 0xd0, 0x17, 0xd4, 0x1f, 0xf4, 0x15,
  0x54, 0x00, 0x00, 0x15, 0x55, 0x1f, 0xfd, 0x15, 0x7d, 0x00, 0x7d, 0x15,
  0x7d, 0x1f, 0xf5, 0x15, 0x54, 0x00, 0x00, 0x15, 0x55, 0x1f, 0x7d, 0x1f,
  0x7d, 0x1f, 0xf5, 0x1f, 0x7d, 0x1f, 0x7d, 0x15, 0x55, 0x00, 0x00, 0x15,
  0x40, 0x1f, 0x40, 0x1f, 0x40, 0x1f, 0x40, 0x1f, 0x55, 0x1f, 0xfd, 0x15,
  0x55, 0x00, 0x00, 0x15, 0x55, 0x1f, 0x7d, 0x1f, 0xfd, 0x1f, 0x7d, 0x1f,
  0x7d, 0x1f, 0x7d, 0x15, 0x55, 0x00, 0x00, 0x15, 0x54, 0x1f, 0xf5, 0x1f,
  0x7d, 0x1f, 0x7d, 0x1f, 0x7d, 0x1f, 0x7d, 0x15, 0x55, 0x00, 0x00, 0x05,
  0x54, 0x17, 0xf5, 0x1f, 0x7d, 0x1f, 0x7d, 0x1f, 0x7d, 0x17, 0xf5, 0x05,
  0x54, 0x00, 0x00, 0x15, 0x54, 0x1f, 0xf5, 0x1f, 0x7d, 0x1f, 0xf5, 0x1f,
  0x54, 0x1f, 0x40, 0x15, 0x40, 0x00, 0x00, 0x05, 0x50, 0x17, 0xd4, 0x1d,
  0x74, 0x1d, 0xf4, 0x1d, 0x75, 0x17, 0xdd, 0x05, 0x55, 0x00, 0x00, 0x15,
  0x54, 0x1f, 0xf5, 0x1f, 0x7d, 0x1f, 0xf5, 0x1f, 0x7d, 0x1f, 0x7d, 0x15,
  0x55, 0x00, 0x00, 0x05, 0x55, 0x17, 0xfd, 0x1f, 0x55, 0x17, 0xf5, 0x15,
  0x7d, 0x1f, 0xf5, 0x15, 0x54, 0x00, 0x00, 0x55, 0x55, 0x7f, 0xfd, 0x57,
  0xd5, 0x07, 0xd0, 0x07, 0xd0, 0x07, 0xd0, 0x05, 0x50, 0x00, 0x00, 0x15,
  0x55, 0x1f, 0x7d, 0x1f, 0x7d, 0x1f, 0x7d, 0x1f, 0x7d, 0x17, 0xf5, 0x05,
  0x54, 0x00, 0x00, 0x15, 0x55, 0x1f, 0x7d, 0x1f, 0x7d, 0x1f, 0x7d, 0x1f,
  0xf5, 0x1f, 0xd4, 0x15, 0x50, 0x00, 0x00, 0x15, 0x55, 0x1f, 0x7d, 0x1f,
  0x7d, 0x1f, 0x7d, 0x1f, 0xfd, 0x1f, 0x7d, 0x15, 0x55, 0x00, 0x00, 0x15,
  0x55, 0x1f, 0x7d, 0x1f, 0x7d, 0x17, 0xf5, 0x1f, 0x7d, 0x1f, 0x7d, 0x15,
  0x55, 0x00, 0x00, 0x15, 0x55, 0x1f, 0x7d, 0x1f, 0x7d, 0x17, 0xfd, 0x15,
  0x7d, 0x1f, 0xf5, 0x15, 0x54, 0x00, 0x00, 0x15, 0x55, 0x1f, 0xfd, 0x15,
  0x7d, 0x17, 0xf5, 0x1f, 0x55, 0x1f, 0xfd, 0x15, 0x55, 0x00, 0x00, 0x15,
  0x54, 0x1f, 0xf4, 0x1f, 0x54, 0x1f, 0x40, 0x1f, 0x54, 0x1f, 0xf4, 0x15,
  0x54, 0x00, 0x00, 0x55, 0x00, 0x7d, 0x40, 0x5f, 0x50, 0x17, 0xd4, 0x05,
  0xf5, 0x01, 0x7d, 0x00, 0x55, 0x00, 0x00, 0x15, 0x54, 0x1f, 0xf4, 0x15,
  0xf4, 0x01, 0xf4, 0x15, 0xf4, 0x1f, 0xf4, 0x15, 0x54, 0x00, 0x00, 0x05,
  0x54, 0x17, 0xf5, 0x1f, 0x7d, 0x15, 0x55, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x15,
  0x55, 0x1f, 0xfd, 0x15, 0x55
};
unsigned int __2048_by_oerg866_8x8s_len = 1025;

struct FontaineFont {
    void *(*malloc_func)(size_t, void *);
    void (*free_func)(void *, void *);
    void *alloc_user_data;
    uint16_t width;
    uint16_t height;
    uint8_t offset;
    uint8_t nchars;
};

#if !defined(FONTAINE_NO_STDLIB)
#include <stdlib.h>

static void *
fontaine_default_malloc(size_t len, void *user_data)
{
    return malloc(len);
}

static void
fontaine_default_free(void *ptr, void *user_data)
{
    free(ptr);
}
#endif /* !defined(FONTAINE_NO_STDLIB) */

struct FontaineFont *
fontaine_new(void *(*malloc_func)(size_t, void *), void (*free_func)(void *, void *), void *alloc_user_data)
{
    const unsigned char *bytes;
    size_t len;
    struct FontaineFont *font;
    unsigned char *pixels;
    int i, y, x, column, row, ro, yo, co, bo, w, h, off, nch;

#if !defined(FONTAINE_NO_STDLIB)
    if (!malloc_func) malloc_func = fontaine_default_malloc;
    if (!free_func) free_func = fontaine_default_free;
#endif /* !defined(FONTAINE_NO_STDLIB) */

    bytes = __2048_by_oerg866_8x8s;
    len = __2048_by_oerg866_8x8s_len;

    off = bytes[0];
    nch = (int)((len - 1) / 16);

    w = 128;
    h = 8 * ((nch + 15) / 16);

    font = malloc_func(sizeof(struct FontaineFont) + w * h, alloc_user_data);
    font->malloc_func = malloc_func;
    font->free_func = free_func;
    font->alloc_user_data = alloc_user_data;
    font->width = w;
    font->height = h;
    font->offset = off;
    font->nchars = nch;

    column = 0;
    row = 0;
    ro = 0;
    co = 0;
    bo = 1;

    pixels = ((unsigned char *)font) + sizeof(*font);

    for (i=0; i<nch; i++) {
        if (column == 16) {
            column = 0;
            co = 0;
            row++;
            ro += 8 * w;
        }

        yo = 0;
        for (y=0; y<8; y++) {
            for (x=0; x<8; x++) {
                pixels[ro + yo + co + x] = ((bytes[bo + (x / 4)] >> (6 - (2 * (x % 4)))) & 0x3) * 85;
            }

            yo += w;
            bo += 2;
        }

        column++;
        co += 8;
    }

    return font;
}

unsigned char *
fontaine_render(struct FontaineFont *font, const char *msg, int *width, int *height)
{
    int y, nch, yr, yw, c, co, ro, bw;
    unsigned char *bitmap;
    unsigned char *pixels;

    nch = (int)strlen(msg);

    *width = nch * 8;
    *height = 8;

    bitmap = font->malloc_func(nch * 8 * 8, font->alloc_user_data);

    bw = font->width;
    pixels = ((unsigned char *)font) + sizeof(*font);

    yr = 0;
    yw = 0;
    for (y=0; y<8; y++) {
        for (c=0; c<nch; c++) {
            co = toupper(msg[c]) - font->offset;
            if (co < 0 || co >= font->nchars) {
                co = 0;
            }

            ro = yr + (co / 16) * 8 * bw + (co % 16) * 8;

            bitmap[yw++] = pixels[ro++];
            bitmap[yw++] = pixels[ro++];
            bitmap[yw++] = pixels[ro++];
            bitmap[yw++] = pixels[ro++];
            bitmap[yw++] = pixels[ro++];
            bitmap[yw++] = pixels[ro++];
            bitmap[yw++] = pixels[ro++];
            bitmap[yw++] = pixels[ro++];
        }

        yr += bw;
    }

    return bitmap;
}

void
fontaine_free_pixels(struct FontaineFont *font, unsigned char *pixels)
{
    font->free_func(pixels, font->alloc_user_data);
}

void
fontaine_free(struct FontaineFont *font)
{
    font->free_func(font, font->alloc_user_data);
}

#endif /* FONTAINE_H */
