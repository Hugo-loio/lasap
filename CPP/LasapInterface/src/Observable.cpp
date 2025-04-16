#include "Observable.h"
#include <fstream>
#include <sstream>
#include <cstdlib>
#include <stdexcept>

using namespace Lasap;

Observable::Observable(
    std::string name,
    std::vector<int> shape,
    std::vector<std::string> keynames,
    std::vector<std::pair<std::string, std::string>> extraprops,
    bool complex_data
    ) {
  numkeys = keynames.size();
  this->keynames = keynames;
  props.push_back({"name", name});
  props.push_back({"complex", (complex_data ? "true" : "false")});
  props.push_back({"rank", std::to_string(shape.size())});
  for (size_t i = 0; i < shape.size(); i++) {
    datasize *= shape[i];
    props.push_back({"dim" + std::to_string(i + 1), std::to_string(shape[i])});
  }    
  props.insert(props.end(), extraprops.begin(), extraprops.end());
  if(complex_data){
    datasize *= 2;
  }
}

int Observable::append(
    const NDArray<double> & array,
    const std::vector<double> & keyvals,
    bool check_duplicate, bool replace) {

  if(array.size != datasize){
    throw std::invalid_argument("Appended array does not match the data expected size.");
  }

  std::vector<double> rowdata(array.size, 0.0);
  for(int i = 0; i < array.size; i++){
    rowdata[i] = double(array.at(i));
  }

  if (check_duplicate) {
    for (auto & row : data) {
      if (std::equal(row.begin(), row.begin() + numkeys, keyvals.begin())) {
	if (replace) {
	  std::copy(rowdata.begin(), rowdata.end(), row.begin() + numkeys);
	  return 1;
	}
	return 2;
      }
    }
  }
  data.push_back(keyvals);
  data.back().insert(data.back().end(), rowdata.begin(), rowdata.end());
  return 0;
}

int Observable::append(
    const NDArray<std::complex<double>> & array,
    const std::vector<double> & keyvals,
    bool check_duplicate, bool replace) {

  if(2*array.size != datasize){
    throw std::invalid_argument("Appended array does not match the data expected size.");
  }

  std::vector<double> rowdata(2*array.size, 0.0);
  for(int i = 0; i < array.size; i++){
    rowdata[i] = double(array.at(i).real());
    rowdata[array.size + i] = double(array.at(i).imag());
  }

  if (check_duplicate) {
    for (auto & row : data) {
      if (std::equal(row.begin(), row.begin() + numkeys, keyvals.begin())) {
	if (replace) {
	  std::copy(rowdata.begin(), rowdata.end(), row.begin() + numkeys);
	  return 1;
	}
	return 2;
      }
    }
  }
  data.push_back(keyvals);
  data.back().insert(data.back().end(), rowdata.begin(), rowdata.end());
  return 0;
}

void Observable::todisk(const std::string& dirname, std::string name, bool verbose, std::string tarname, std::string diskformat) {
  std::string path = data_dir();
  check_dir(path);
  path += dirname;
  check_dir(path);

  if (name.empty()) name = props[0].second;

  std::string name_props = name + "_props." + diskformat;
  std::string name_data = name + "_data." + diskformat;

  std::string path_props = path + "/" + name_props;
  std::string path_data = path + "/" + name_data;

  if (diskformat == "csv") {
    std::ofstream props_file(path_props);

    props_file << props[0].first;
    for (size_t i = 1; i < props.size(); i++) {
      props_file << "," << props[i].first;
    }
    props_file << "\n";

    props_file << props[0].second;
    for (size_t i = 1; i < props.size(); i++) {
      props_file << "," << props[i].second;
    }
    props_file << "\n";

    props_file.close();


    std::ofstream data_file(path_data);
    data_file.precision(std::numeric_limits<double>::max_digits10);

    for(const auto & keyname: keynames){
      data_file << keyname << ",";
    }

    for(size_t i = 1; i <= datasize; i++){
      data_file << i << (i == datasize ? "\n" : ",");
    }

    for(const auto& row : data){
      for(size_t i = 0; i < row.size(); ++i){
	data_file << row[i] << (i + 1 < row.size() ? "," : "\n");
      }
    }
    data_file.close();
  }

  if(verbose){
    std::cout << "Outputted data files to: " << path << "/" << name << std::endl;
  }

  if (!tarname.empty()) {
    std::string tarpath = path + "/" + tarname + ".tar";

    std::string tar_command = "tar -rf " + tarpath + " -C " + path + " " + name_props + " " + name_data;
    std::system(tar_command.c_str());

    std::remove(path_props.c_str());
    std::remove(path_data.c_str());

    if (verbose) {
      std::cout << "Bundled into archive: " << tarpath << std::endl;
    }
  }
}

std::string Observable::data_dir() {
  const char * env_p = std::getenv("LASAP_DATA_DIR");
  if (env_p) {
    std::string path(env_p);
    if (path.back() != '/') path += "/";
    return path;
  }
  return std::filesystem::current_path().string() + "/data/";
}

void Observable::check_dir(const std::string & dir) {
  if (! std::filesystem::exists(dir)) {
    std::filesystem::create_directories(dir);
  }
}
