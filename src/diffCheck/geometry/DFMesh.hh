#pragma once

#include <Eigen/Core>
#include <open3d/Open3D.h>

#include "diffCheck/geometry/DFPointCloud.hh"
#include "diffCheck/transformation/DFTransformation.hh"

namespace diffCheck::geometry
{
    class DFMesh
    {
    public:
        DFMesh() {}
        DFMesh(std::vector<Eigen::Vector3d> vertices,
               std::vector<Eigen::Vector3i> faces,
               std::vector<Eigen::Vector3d> normalsVertex,
               std::vector<Eigen::Vector3d> normalsFace,
               std::vector<Eigen::Vector3d> colorsVertex)
            : 
            Vertices(vertices),
            Faces(faces),
            NormalsVertex(normalsVertex),
            NormalsFace(normalsFace),
            ColorsVertex(colorsVertex)
        {
            this->ColorsFace.resize(faces.size());
            this->ColorsFace.assign(faces.size(), Eigen::Vector3d(0, 0, 0));
        }
        
        ~DFMesh() = default;

    public:  ///< Convertes
        /**
         * @brief Convert a open3d triangle mesh to our datatype
         * 
         * @param std::shared_ptr<open3d::geometry::TriangleMesh> the shared pointer of the open3d triangle mesh
         */
        void Cvt2DFMesh(const std::shared_ptr<open3d::geometry::TriangleMesh> &O3DTriangleMesh);

        /**
         * @brief Convert the DFMesh to open3d triangle mesh
         * 
         * @return std::shared_ptr<open3d::geometry::TriangleMesh> the open3d triangle mesh
         */
        std::shared_ptr<open3d::geometry::TriangleMesh> Cvt2O3DTriangleMesh();

    public:  ///< Mesh methods
        /**
         * @brief Sample the mesh uniformly with a target number of points
         * 
         * @param numPoints the number of points to sample
         * @return std::shared_ptr<geometry::DFPointCloud> the sampled point cloud
         */
        std::shared_ptr<diffCheck::geometry::DFPointCloud> SampleCloudUniform(int numPoints = 1000);

    public:  ///< Transformers
        /**
         * @brief Apply a transformation to the mesh
         * 
         * @param transformation the transformation to apply
         */
        void ApplyTransformation(const diffCheck::transformation::DFTransformation &transformation);

    public:  ///< Utils
        /**
         * @brief Get the mesh tight bounding box
         * 
         * @return std::vector<Eigen::Vector3d> A vector of two Eigen::Vector3d, with the first one being the minimum
         * point and the second one the maximum point of the bounding box.
         */
        std::vector<Eigen::Vector3d> GetTightBoundingBox();

        /**
         * @brief Get the first normal of the mesh. Meant for planar meshes
         * 
         * @return Eigen::Vector3d the normal
         */
        Eigen::Vector3d GetFirstNormal();

        /**
         * @brief Check if a point is on a face of the mesh
         * 
         * @param point the point to check
         * @param associationThreshold the threshold to consider the point associable to the mesh. It is the ratio between the surface of the closest mesh triangle of the mesh face, and the sum of the areas of the three triangles described by the point projected on the mesh face and two of the mesh triangle vertices. The lower the number, the more strict the association will be and some poinnts on the mesh face might be wrongfully excluded. In theory, in a perfect case, a value of 0 could be used, but in practice, values of 0.05-0.2 are more realistic, depending on the application.
         */
        bool IsPointOnFace(Eigen::Vector3d point, double associationThreshold = 0.1);

        /**
         * @brief Get the center and main axis of oriented boundung box of the mesh. It was developped for the cylinder case, but can be used for other shapes.
         * 
         * @return std::tuple<Eigen::Vector3d, Eigen::Vector3d> the first element is the center of the obb of the mesh, the second element is the main axis of the obb of the mesh
         */
        std::tuple<Eigen::Vector3d, Eigen::Vector3d> GetCenterAndAxis();

    public:  ///< I/O loader
        /**
         * @brief Read a mesh from a file
         * 
         * @param filename the path to the file with the extension
         */
        void LoadFromPLY(const std::string &path);

    public:  ///< Getters
        /// @brief Number of vertices in the mesh
        int GetNumVertices() const { return this->Vertices.size(); }
        /// @brief Number of faces in the mesh
        int GetNumFaces() const { return this->Faces.size(); }

    public:  ///< Distance calculations
        /**
         * @brief Compute the distance between the df mesh and a df point cloud. It
         * can be considered as a point to plane distance.
         * 
         * @param target the target cloud in format df
         * @param useAbs if true, the absolute value of the distance is returned
         * @return std::vector<float> the distance between the point cloud and the mesh
         */
        std::vector<float> ComputeDistance(const diffCheck::geometry::DFPointCloud &targetMesh, bool useAbs = true);


    public:  ///< Basic mesh data
        /// @brief Eigen vector of 3D vertices
        std::vector<Eigen::Vector3d> Vertices;
        /// @brief Eigen vector of faces
        std::vector<Eigen::Vector3i> Faces;
        /// @brief Eigen vector of 3D vertices normals
        std::vector<Eigen::Vector3d> NormalsVertex;
        /// @brief Eigen vector of faces normals
        std::vector<Eigen::Vector3d> NormalsFace;
        /// @brief Eigen vector of 3D colors for vertices
        std::vector<Eigen::Vector3d> ColorsVertex;
        /// @brief Eigen vector of 3D colors for faces
        std::vector<Eigen::Vector3d> ColorsFace;
    };
} // namespace diffCheck::geometry