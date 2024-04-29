// diffCheck_py.cc
#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include <pybind11/stl.h>

#include "diffCheck.hh"

namespace py = pybind11;


PYBIND11_MODULE(diffCheckBindings, m) {
    m.doc() = "diffCheck python bindings"; // optional module docstring

    py::class_<diffCheck::geometry::DFPointCloud>(m, "DFPointCloud")
        .def(py::init<>())
        .def(py::init<std::vector<Eigen::Vector3d>, std::vector<Eigen::Vector3d>, std::vector<Eigen::Vector3d>>())
        .def("Cvt2DFPointCloud", &diffCheck::geometry::DFPointCloud::Cvt2DFPointCloud)
        .def("Cvt2O3DPointCloud", &diffCheck::geometry::DFPointCloud::Cvt2O3DPointCloud)
        .def("ComputeP2PDistance", &diffCheck::geometry::DFPointCloud::ComputeP2PDistance)
        .def("ComputeBoundingBox", &diffCheck::geometry::DFPointCloud::ComputeBoundingBox)

        .def("get_num_points", &diffCheck::geometry::DFPointCloud::GetNumPoints);
}


// #include <pybind11/pybind11.h>

// int add(int i, int j) {
//     return i + j;
// }

// PYBIND11_MODULE(diffCheckBindings, m) {
//     m.def("add", &add, "A function which adds two numbers");
// }