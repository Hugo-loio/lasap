#include "Progress.h"
#include <iomanip>
#include <cmath>
#include <thread>

Lasap::Progress::Progress(int niterations, double divisor)
    : niterations(niterations), divisor(divisor) {
    interval = std::ceil(niterations / divisor);
    start_time = std::chrono::steady_clock::now();
}

bool Lasap::Progress::print_progress(int count) {
    if (count % interval == 0 || count == niterations) {
        // Calculate elapsed time in milliseconds
        auto elapsed_time = std::chrono::steady_clock::now() - start_time;
        auto elapsed_ms = std::chrono::duration_cast<std::chrono::milliseconds>(elapsed_time).count();
        
        // Convert elapsed time to hours, minutes, and seconds
        int hours = static_cast<int>(elapsed_ms / (1000 * 3600));
        int minutes = static_cast<int>((elapsed_ms / (1000 * 60)) % 60);
        int seconds = static_cast<int>((elapsed_ms / 1000) % 60);
        
        // Print the progress and elapsed time in HH:MM:SS format
        std::cout << std::fixed << std::setprecision(0)
                  << round(100.0 * count / niterations) << " % at "
                  << hours << ":"
                  << std::setw(2) << std::setfill('0') << minutes << ":"
                  << std::setw(2) << std::setfill('0') << seconds
                  << std::endl;
        
        return true;
    }
    return false;
}
