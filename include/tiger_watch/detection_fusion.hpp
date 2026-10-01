#pragma once
#include <string>

namespace tiger_watch {

class DetectionFusion {
public:
    DetectionFusion(const std::string& engine_path);
    ~DetectionFusion();
    void run();
private:
    DetectionFusion* fusion_ = nullptr;
  
};

} // namespace tiger_watch
