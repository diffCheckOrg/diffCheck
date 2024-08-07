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
    // dfb_geometry namespace
    //#################################################################################################

    py::module_ submodule_geometry = m.def_submodule("dfb_geometry", "A submodule for wrap geometries in df.");

    py::class_<diffCheck::geometry::DFPointCloud, std::shared_ptr<diffCheck::geometry::DFPointCloud>>(submodule_geometry, "DFPointCloud",
        "A class for the point cloud representation.")
        .def(py::init<>())
        .def(py::init<std::vector<Eigen::Vector3d>, std::vector<Eigen::Vector3d>, std::vector<Eigen::Vector3d>>(),
            py::arg("points"), py::arg("colors"), py::arg("normals"))
        
        .def("compute_distance", &diffCheck::geometry::DFPointCloud::ComputeDistance,
            py::arg("target_cloud"))
        .def("compute_BoundingBox", &diffCheck::geometry::DFPointCloud::ComputeBoundingBox)
        
        .def("voxel_downsample", &diffCheck::geometry::DFPointCloud::VoxelDownsample,
            py::arg("voxel_size"))
        .def("uniform_downsample", &diffCheck::geometry::DFPointCloud::UniformDownsample,
            py::arg("every_k_points"))
        .def("downsample_by_size", &diffCheck::geometry::DFPointCloud::DownsampleBySize,
            py::arg("target_size"))

        .def("estimate_normals", &diffCheck::geometry::DFPointCloud::EstimateNormals,
            py::arg("use_cilantro_evaluator") = false,
            py::arg("knn") = 100,
            py::arg("search_radius") = std::nullopt)

        .def("apply_color", (void (diffCheck::geometry::DFPointCloud::*)(int, int, int)) &diffCheck::geometry::DFPointCloud::ApplyColor,
            py::arg("r"), py::arg("g"), py::arg("b"))

        .def("load_from_PLY", &diffCheck::geometry::DFPointCloud::LoadFromPLY)
        .def("add_points", &diffCheck::geometry::DFPointCloud::AddPoints)

        .def("get_tight_bounding_box", &diffCheck::geometry::DFPointCloud::GetTightBoundingBox)

        .def("get_num_points", &diffCheck::geometry::DFPointCloud::GetNumPoints,
            "Get the number of points in the point cloud.")
        .def("get_num_colors", &diffCheck::geometry::DFPointCloud::GetNumColors)
        .def("get_num_normals", &diffCheck::geometry::DFPointCloud::GetNumNormals)
        .def("get_center_point", &diffCheck::geometry::DFPointCloud::GetCenterPoint)

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

    py::class_<diffCheck::geometry::DFMesh, std::shared_ptr<diffCheck::geometry::DFMesh>>(submodule_geometry, "DFMesh",
        "A class for the triangle mesh representation.")
        .def(py::init<>())
        .def(py::init<std::vector<Eigen::Vector3d>, std::vector<Eigen::Vector3i>, std::vector<Eigen::Vector3d>, std::vector<Eigen::Vector3d>, std::vector<Eigen::Vector3d>>())

        .def("compute_distance", &diffCheck::geometry::DFMesh::ComputeDistance,
            py::arg("target_cloud"),
            py::arg("is_abs") = true)
            
        .def("load_from_PLY", &diffCheck::geometry::DFMesh::LoadFromPLY)

        .def("sample_points_uniformly", &diffCheck::geometry::DFMesh::SampleCloudUniform)

        .def("get_tight_bounding_box", &diffCheck::geometry::DFMesh::GetTightBoundingBox)

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
    
    //#################################################################################################
    // dfb_transformation namespace
    //#################################################################################################

    py::module_ submodule_transformation = m.def_submodule("dfb_transformation", "A submodule for the transformation classes.");

    py::class_<diffCheck::transformation::DFTransformation>(submodule_transformation, "DFTransformation")
        .def(py::init<>())
        .def(py::init<const Eigen::Matrix4d&>())

        .def_readwrite("transformation_matrix", &diffCheck::transformation::DFTransformation::TransformationMatrix);

    //#################################################################################################
    // dfb_registrations namespace
    //#################################################################################################

    py::module_ submodule_registrations = m.def_submodule("dfb_registrations", "A submodule for the registration methods.");

    py::class_<diffCheck::registrations::DFGlobalRegistrations>(submodule_registrations, "DFGlobalRegistrations",
        "A static class for the global registration methods.")
        .def_static("O3DFastGlobalRegistrationFeatureMatching", &diffCheck::registrations::DFGlobalRegistrations::O3DFastGlobalRegistrationFeatureMatching,
            py::arg("source"),
            py::arg("target"),
            py::arg("voxelize") = false,
            py::arg("voxel_size") = 0.005,
            py::arg("radius_kd_tree_search") = 0.8,
            py::arg("max_neighbor_kd_tree_search") = 50,
            py::arg("max_correspondence_distance") = 0.05,
            py::arg("iteration_number") = 128,
            py::arg("max_tuple_count") = 1000)
        .def_static("O3DRansacOnFeatureMatching", &diffCheck::registrations::DFGlobalRegistrations::O3DRansacOnFeatureMatching,
            py::arg("source"),
            py::arg("target"),
            py::arg("voxelize") = false,
            py::arg("voxel_size") = 0.005,
            py::arg("radius_kd_tree_search") = 1.0,
            py::arg("max_neighbor_kd_tree_search") = 50,
            py::arg("max_correspondence_distance") = 0.5,
            py::arg("is_t_estimate_pt2pt") = false,
            py::arg("ransac_n") = 3,
            py::arg("correspondence_checker_distance") = 0.05,
            py::arg("similarity_threshold") = 1.5,
            py::arg("ransac_max_iteration") = 5000,
            py::arg("ransac_confidence_threshold") = 0.999);

    py::class_<diffCheck::registrations::DFRefinedRegistration>(submodule_registrations, "DFRefinedRegistration",
        "A static class for the refined registration methods.")
        .def_static("O3DICP", &diffCheck::registrations::DFRefinedRegistration::O3DICP,
            py::arg("source"),
            py::arg("target"),
            py::arg("max_correspondence_distance") = 0.1,
            py::arg("is_t_estimate_pt2pt") = false,
            py::arg("relative_fitness") = 1e-6,
            py::arg("relative_rmse") = 1e-6,
            py::arg("max_iteration") = 30,
            py::arg("use_point_to_plane") = false)
        .def_static("O3DGeneralizedICP", &diffCheck::registrations::DFRefinedRegistration::O3DGeneralizedICP,
            py::arg("source"),
            py::arg("target"),
            py::arg("max_correspondence_distance") = 0.1,
            py::arg("max_iteration") = 30,
            py::arg("relative_fitness") = 1e-6,
            py::arg("relative_rmse") = 1e-6);

    //#################################################################################################
    // dfb_segmentation namespace
    //#################################################################################################

    py::module_ submodule_segmentation = m.def_submodule("dfb_segmentation", "A submodule for the `semantic` segmentation methods.");

    py::class_<diffCheck::segmentation::DFSegmentation>(submodule_segmentation, "DFSegmentation",
        "A static class for the segmentation methods.")
        .def_static("segment_by_normal", &diffCheck::segmentation::DFSegmentation::NormalBasedSegmentation,
            py::arg("point_cloud"),
            py::arg("normal_threshold_degree") = 20.0,
            py::arg("min_cluster_size") = 10,
            py::arg("use_knn_neighborhood") = true,
            py::arg("knn_neighborhood_size") = 10,
            py::arg("radius_neighborhood_size") = 0.1,
            py::arg("color_clusters") = false)
        
        .def_static("associate_clusters", &diffCheck::segmentation::DFSegmentation::AssociateClustersToMeshes,
            py::arg("reference_mesh"),
            py::arg("unassociated_clusters"),
            py::arg("angle_threshold") = 0.1,
            py::arg("association_threshold") = 0.1)
        
        .def_static("clean_unassociated_clusters", &diffCheck::segmentation::DFSegmentation::CleanUnassociatedClusters,
            py::arg("unassociated_clusters"),
            py::arg("associated_clusters"),
            py::arg("reference_mesh"),
            py::arg("angle_threshold") = 0.1,
            py::arg("association_threshold") = 0.1);
}
