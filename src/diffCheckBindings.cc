// diffCheck_py.cc
#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include <pybind11/stl.h>

#include "diffCheck.hh"

namespace py = pybind11;

bool test() { return true; }

PYBIND11_MODULE(diffcheck_bindings, m) {
    m.doc() = "The diffcheck bindings for python.";

    //#################################################################################################
    // testing namespace
    //#################################################################################################

    py::module_ submodule_test = m.def_submodule("dfb_test", "A submodule for testing the python bindings.");
    submodule_test.def("test", &test, "Simple function testing a vanilla python bindings.");

    //#################################################################################################
    // df_geometry namespace
    //#################################################################################################

    py::module_ submodule_geometry = m.def_submodule("dfb_geometry", "A submodule for the geometry classes.");

    py::class_<diffCheck::geometry::DFPointCloud, std::shared_ptr<diffCheck::geometry::DFPointCloud>>(submodule_geometry, "DFPointCloud")
        .def(py::init<>())
        .def(py::init<std::vector<Eigen::Vector3d>, std::vector<Eigen::Vector3d>, std::vector<Eigen::Vector3d>>())
        
        .def("compute_P2PDistance", &diffCheck::geometry::DFPointCloud::ComputeP2PDistance)
        .def("compute_BoundingBox", &diffCheck::geometry::DFPointCloud::ComputeBoundingBox)

        .def("load_from_PLY", &diffCheck::geometry::DFPointCloud::LoadFromPLY)

        .def("get_num_points", &diffCheck::geometry::DFPointCloud::GetNumPoints)
        .def("get_num_colors", &diffCheck::geometry::DFPointCloud::GetNumColors)
        .def("get_num_normals", &diffCheck::geometry::DFPointCloud::GetNumNormals)

        .def("has_points", &diffCheck::geometry::DFPointCloud::HasPoints)
        .def("has_colors", &diffCheck::geometry::DFPointCloud::HasColors)
        .def("has_normals", &diffCheck::geometry::DFPointCloud::HasNormals)

        .def_property("points",
            [](const diffCheck::geometry::DFPointCloud &self) { return self.Points; },
            [](diffCheck::geometry::DFPointCloud &self, const std::vector<Eigen::Vector3d>& value) { self.Points = value; })
        .def_property("colors",
            [](const diffCheck::geometry::DFPointCloud &self) { return self.Colors; },
            [](diffCheck::geometry::DFPointCloud &self, const std::vector<Eigen::Vector3d>& value) { self.Colors = value; })
        .def_property("normals",
            [](const diffCheck::geometry::DFPointCloud &self) { return self.Normals; },
            [](diffCheck::geometry::DFPointCloud &self, const std::vector<Eigen::Vector3d>& value) { self.Normals = value; });

    py::class_<diffCheck::geometry::DFMesh, std::shared_ptr<diffCheck::geometry::DFMesh>>(submodule_geometry, "DFMesh")
        .def(py::init<>())
        .def(py::init<std::vector<Eigen::Vector3d>, std::vector<Eigen::Vector3i>, std::vector<Eigen::Vector3d>, std::vector<Eigen::Vector3d>, std::vector<Eigen::Vector3d>>())

        .def("load_from_PLY", &diffCheck::geometry::DFMesh::LoadFromPLY)

        .def("sample_points_uniformly", &diffCheck::geometry::DFMesh::SampleCloudUniform)

        .def("get_num_vertices", &diffCheck::geometry::DFMesh::GetNumVertices)
        .def("get_num_faces", &diffCheck::geometry::DFMesh::GetNumFaces)

        .def_property("vertices",
            [](const diffCheck::geometry::DFMesh &self) { return self.Vertices; },
            [](diffCheck::geometry::DFMesh &self, const std::vector<Eigen::Vector3d>& value) { self.Vertices = value; })
        .def_property("faces",
            [](const diffCheck::geometry::DFMesh &self) { return self.Faces; },
            [](diffCheck::geometry::DFMesh &self, const std::vector<Eigen::Vector3i>& value) { self.Faces = value; })
        .def_property("normals_vertex",
            [](const diffCheck::geometry::DFMesh &self) { return self.NormalsVertex; },
            [](diffCheck::geometry::DFMesh &self, const std::vector<Eigen::Vector3d>& value) { self.NormalsVertex = value; })
        .def_property("normals_face",
            [](const diffCheck::geometry::DFMesh &self) { return self.NormalsFace; },
            [](diffCheck::geometry::DFMesh &self, const std::vector<Eigen::Vector3d>& value) { self.NormalsFace = value; })
        .def_property("colors_vertex",
            [](const diffCheck::geometry::DFMesh &self) { return self.ColorsVertex; },
            [](diffCheck::geometry::DFMesh &self, const std::vector<Eigen::Vector3d>& value) { self.ColorsVertex = value; })
        .def_property("colors_face",
            [](const diffCheck::geometry::DFMesh &self) { return self.ColorsFace; },
            [](diffCheck::geometry::DFMesh &self, const std::vector<Eigen::Vector3d>& value) { self.ColorsFace = value; });
    
    // //#################################################################################################
    // // df_registration namespace
    // //#################################################################################################

    // py::module_ submodule_geometry = m.def_submodule("df_registration", "A submodule for the registration methods.");
}