#ifndef PROGRESS_H
#define PROGRESS_H

#include <chrono>
#include <iostream>

namespace Lasap {
  class Progress {
    public:
      int niterations;
      double divisor;
      int interval;
      std::chrono::steady_clock::time_point start_time;

      Progress(int niterations, double divisor = 10);

      bool print_progress(int count);
  };
}

#endif 
