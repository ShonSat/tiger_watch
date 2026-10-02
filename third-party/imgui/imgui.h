#pragma once

#include <cstdarg>

struct ImVec2 {
    float x;
    float y;
    ImVec2(float x_ = 0.0f, float y_ = 0.0f) : x(x_), y(y_) {}
};

struct ImVec4 {
    float x;
    float y;
    float z;
    float w;
    ImVec4(float x_ = 0.0f, float y_ = 0.0f, float z_ = 0.0f, float w_ = 1.0f)
        : x(x_), y(y_), z(z_), w(w_) {}
};

enum ImGuiCol_ {
    ImGuiCol_WindowBg = 0,
    ImGuiCol_TitleBg,
    ImGuiCol_TitleBgActive,
    ImGuiCol_FrameBg,
    ImGuiCol_FrameBgHovered,
    ImGuiCol_FrameBgActive,
    ImGuiCol_CheckMark,
    ImGuiCol_SliderGrab,
    ImGuiCol_COUNT
};

enum ImGuiWindowFlags_ {
    ImGuiWindowFlags_NoCollapse = 1 << 0,
    ImGuiWindowFlags_NoScrollbar = 1 << 1,
    ImGuiWindowFlags_NoSavedSettings = 1 << 2,
    ImGuiWindowFlags_NoResize = 1 << 3,
    ImGuiWindowFlags_NoMove = 1 << 4,
    ImGuiWindowFlags_NoTitleBar = 1 << 5,
    ImGuiWindowFlags_NoBringToFrontOnFocus = 1 << 6,
    ImGuiWindowFlags_NoFocusOnAppearing = 1 << 7,
    ImGuiWindowFlags_AlwaysUseWindowPadding = 1 << 8,
    ImGuiWindowFlags_AlwaysAutoResize = 1 << 9
};

enum ImGuiSliderFlags_ {
    ImGuiSliderFlags_Logarithmic = 1 << 0
};

struct ImDrawData {};

struct ImGuiStyle {
    float WindowRounding = 0.0f;
    float WindowBorderSize = 0.0f;
    ImVec4 Colors[ImGuiCol_COUNT] = {};
};

namespace ImGui {
    inline void* GetCurrentContext() { return nullptr; }

    inline ImGuiStyle& GetStyle() {
        static ImGuiStyle style{};
        return style;
    }

    inline void SetNextWindowBgAlpha(float) {}
    inline void SetNextWindowSize(const ImVec2&, const ImVec2& = ImVec2()) {}
    inline void SetNextWindowPos(const ImVec2&) {}
    inline bool Begin(const char*, void* = nullptr, int = 0) { return true; }
    inline void End() {}
    inline void Text(const char*, ...) {}
    template <typename T>
    inline bool SliderFloat(const char*, T*, float, float, const char* = nullptr, int = 0) {
        return false;
    }
    inline void SetItemDefaultFocus() {}
    inline ImDrawData* GetDrawData() { return nullptr; }
}
