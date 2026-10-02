#pragma once

struct ImDrawData;

extern "C" {
    bool ImGui_ImplOpenGL3_Init(const char* glsl_version = nullptr);
    void ImGui_ImplOpenGL3_Shutdown(void);
    void ImGui_ImplOpenGL3_NewFrame(void);
    void ImGui_ImplOpenGL3_RenderDrawData(ImDrawData* draw_data);
}
