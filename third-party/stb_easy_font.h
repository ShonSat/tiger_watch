#pragma once

#include <cstring>

#ifdef __cplusplus
extern "C" {
#endif

int stb_easy_font_print(float x, float y, char *text, void *m, void *buffer, int buffer_size);
int stb_easy_font_width(char *text);

#ifdef __cplusplus
}
#endif

inline int stb_easy_font_width(char *text)
{
    if (!text)
        return 0;
    return static_cast<int>(std::strlen(text)) * 7;
}
