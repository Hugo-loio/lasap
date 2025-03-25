#ifndef NDARRAY_H
#define NDARRAY_H

#include <vector>

namespace Lasap {

  template <typename T>
    class NDArray {
      public:
	NDArray(std::vector<int> shape);
	~NDArray();
	NDArray(const NDArray<T> & other);
	T & operator[](const std::vector<int>& indices);
	T & operator[](int index);
	const T at(int index) const;

	void reshape(std::vector<int> new_shape);
	void display();

	int size = 1;
	std::vector<int> shape;

      protected:
	T * array = nullptr;

	int get_flat_index(const std::vector<int> & indices) const;
	void display_closing_brackets(int depth) const;
	void display_opening_brackets(int depth) const;

    };

}

#endif

