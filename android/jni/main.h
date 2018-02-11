#pragma once

struct TouchEvent {
    int pressed;
    float x;
    float y;
    int finger;
};

void evt_push(struct TouchEvent *in);
int evt_pop(struct TouchEvent *out);

int androidsound_load(const char *filename);
void androidsound_play(int id);
