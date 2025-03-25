#include <iostream>
#include <stdexcept>
#include <complex>

#include "NDArray.h"

using namespace Lasap;

template <typename T>
NDArray<T>::NDArray(std::vector<int> shape){
  this->shape = shape;
  for (int dim : shape) {
    size *= dim;
  }
  array = new T[size];
}

template <typename T>
NDArray<T>::~NDArray() {
  delete[] array;
}

template <typename T>
NDArray<T>::NDArray(const NDArray<T>& other) {
  shape = other.shape;
  for (int dim : shape) {
    size *= dim;
  }
  array = new T[size];
  std::copy(other.array, other.array + size, array);
}

template <typename T>
void NDArray<T>::reshape(std::vector<int> new_shape) {
  int new_size = 1;
  for (int dim : new_shape) {
    new_size *= dim;
  }

  if (new_size == size) {
    shape = new_shape;
  } else {
    throw std::invalid_argument("New shape must have the same total dimension.");
  }
}

template <typename T>
int NDArray<T>::get_flat_index(const std::vector<int> & indices) const {
  if (indices.size() != shape.size()) {
    throw std::out_of_range("Index dimensionality mismatch.");
  }

  int flat_index = 0;
  int multiplier = 1;
  for (int i = shape.size() - 1; i >= 0; --i) {
    if (indices[i] < 0 || indices[i] >= shape[i]) {
      throw std::out_of_range("Index out of bounds.");
    }
    flat_index += indices[i] * multiplier;
    multiplier *= shape[i];
  }
  return flat_index;
}

template <typename T>
T & NDArray<T>::operator[](const std::vector<int>& indices) {
  return array[get_flat_index(indices)];
}

template <typename T>
T & NDArray<T>::operator[](int index) {
  return array[index];
}

template <typename T>
const T NDArray<T>::at(int index) const {
  return array[index];
}

template <typename T>
void NDArray<T>::display_closing_brackets(int depth) const {
  std::cout << "]" << std::endl;
  for(int i = shape.size() - 2; i >= depth; i--){
    for(int e = 0; e < i; e++){
      std::cout << " " ; 
    }
    std::cout << "]" << std::endl;
  }
}

template <typename T>
void NDArray<T>::display_opening_brackets(int depth) const {
  for(int i = depth; i < shape.size(); i++){
    for(int e = 0; e < i; e++){
      std::cout << " ";
    }
    std::cout << "[";
    if(i < shape.size() - 1){
      std::cout << std::endl;
    }
  }
}

template <typename T>
void NDArray<T>::display() {
  int depth = shape.size();
  std::vector<int> indices(depth, 0);

  std::cout.precision(std::numeric_limits<double>::max_digits10);

  display_opening_brackets(0);
  while(true){
    std::cout << (*this)[indices];
    if(indices.back() < this->shape.back() - 1){
      std::cout << " ";
    }

    int i = depth - 1;
    // Increment indices
    for(i; i >= 0; i--){
      indices[i] = (indices[i] + 1) % shape[i];
      if(indices[i] != 0){
	break;
      }
    }

    if(i == -1){
      break;
    }
    if(i < depth - 1){
      display_closing_brackets(i + 1);
      display_opening_brackets(i + 1);
    }
  }
  display_closing_brackets(0);
}

template class NDArray<double>;
template class NDArray<std::complex<double>>;
