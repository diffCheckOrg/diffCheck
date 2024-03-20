#pragma once

#include <Eigen/Core>
#include <open3d/Open3D.h>

namespace diffCheck::geometry
{
    class DFMesh
    {
    public:
        DFMesh() = default;
        ~DFMesh() = default;

    ///< Convertes
    public:
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

    ///< I/O loader
    public:
        /**
         * @brief Read a mesh from a file
         * 
         * @param filename the path to the file with the extension
         */
        void LoadFromPLY(const std::string &path);

    ///< Getters
    public:
        /// @brief Number of vertices in the mesh
        int GetNumVertices() const { return this->Vertices.size(); }
        /// @brief Number of faces in the mesh
        int GetNumFaces() const { return this->Faces.size(); }

    ///< Basic mesh data
    public:
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