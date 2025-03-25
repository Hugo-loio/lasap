#ifndef OBSERVABLE_H
#define OBSERVABLE_H

#include <iostream>
#include <vector>
#include <filesystem>
#include <complex>

#include "NDArray.h"

namespace Lasap {

  class Observable {
    public:
      Observable(
	  std::string name, 
	  std::vector<int> shape, 
	  std::vector<std::string> keynames = {}, 
	  std::vector<std::pair<std::string, std::string>> extraprops = {},
	  bool complex_data = false
	  );

      int append(
	  const NDArray<double> & array,
	  const std::vector<double> & keyvals,
	  bool check_duplicate = false,
	  bool replace = false
	  ); 

      int append(
	  const NDArray<std::complex<double>> & array,
	  const std::vector<double> & keyvals,
	  bool check_duplicate = false,
	  bool replace = false
	  ); 

      void todisk(
	  const std::string& dirname, 
	  std::string name = "", 
	  bool verbose = false, 
	  std::string tarname = "", 
	  std::string diskformat = "csv"
	  );

    protected:
      std::vector<std::pair<std::string, std::string>> props;
      std::vector<std::vector<double>> data;
      std::vector<std::string> keynames;
      int numkeys;
      int datasize = 1;

      static std::string data_dir();
      void check_dir(const std::string & dir);
  };

}

using namespace Lasap;

#endif
