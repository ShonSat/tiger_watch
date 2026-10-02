#pragma once

#include "imgui.h"

struct GLFWwindow;

extern "C" {
    int ImGui_ImplGlfw_InitForOpenGL(GLFWwindow* window, bool install_callbacks);
    void ImGui_ImplGlfw_Shutdown(void);
    void ImGui_ImplGlfw_NewFrame(void);
    void ImGui_ImplGlfw_MouseButtonCallback(GLFWwindow* window, int button, int action, int mods);
    void ImGui_ImplGlfw_ScrollCallback(GLFWwindow* window, double xoffset, double yoffset);
    void ImGui_ImplGlfw_CursorPosCallback(GLFWwindow* window, double x, double y);
    void ImGui_ImplGlfw_KeyCallback(GLFWwindow* window, int key, int scancode, int action, int mods);
}

inline int ImGui_ImplGlfw_InitForOpenGL(GLFWwindow*, bool) { return 0; }
inline void ImGui_ImplGlfw_Shutdown(void) {}
inline void ImGui_ImplGlfw_NewFrame(void) {}
inline void ImGui_ImplGlfw_MouseButtonCallback(GLFWwindow*, int, int, int) {}
inline void ImGui_ImplGlfw_ScrollCallback(GLFWwindow*, double, double) {}
inline void ImGui_ImplGlfw_CursorPosCallback(GLFWwindow*, double, double) {}
inline void ImGui_ImplGlfw_KeyCallback(GLFWwindow*, int, int, int, int) {}
