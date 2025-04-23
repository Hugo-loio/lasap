#ifndef NDARRAY_H
#define NDARRAY_H

#include <vector>

namespace Lasap {

  template <typename T>
    class NDArray {
      public:
	NDArray(std::vector<int> shape);
	NDArray(std::vector<int> shape, T val);
	~NDArray();
	NDArray(const NDArray<T> & other);

	NDArray<T>& operator+= (const NDArray<T> & other);
	NDArray<T> operator+ (const NDArray<T> & other) const;
	NDArray<T>& operator+=(const T& scalar);
	NDArray<T> operator+(const T& scalar) const;

	NDArray<T>& operator-= (const NDArray<T> & other);
	NDArray<T> operator- (const NDArray<T> & other) const;
	NDArray<T>& operator-=(const T& scalar);
	NDArray<T> operator-(const T& scalar) const;

	NDArray<T>& operator*= (const NDArray<T> & other);
	NDArray<T> operator* (const NDArray<T> & other) const;
	NDArray<T>& operator*=(const T& scalar);
	NDArray<T> operator*(const T& scalar) const;

	NDArray<T>& operator/= (const NDArray<T> & other);
	NDArray<T> operator/ (const NDArray<T> & other) const;
	NDArray<T>& operator/=(const T& scalar);
	NDArray<T> operator/(const T& scalar) const;

	NDArray<T> & operator= (const NDArray<T> & other);

	T & operator[](const std::vector<int>& indices);
	T & operator[](int index);
	const T & operator[](int index) const;
	const T at(int index) const;

	void reshape(std::vector<int> new_shape);
	void display();

	int getSize() const{return size;};
	std::vector<int> getShape() const{return shape;}

      protected:
	T * array = nullptr;
	std::vector<int> shape;
	int size = 1;

	int get_flat_index(const std::vector<int> & indices) const;
	void display_closing_brackets(int depth) const;
	void display_opening_brackets(int depth) const;
	void check_shapes(std::vector<int> shape1, std::vector<int> shape2);

    };

}

#endif

