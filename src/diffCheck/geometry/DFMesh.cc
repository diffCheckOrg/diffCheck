#include "diffCheck/geometry/DFMesh.hh"
#include "diffCheck/IOManager.hh"

#include <open3d/t/geometry/RaycastingScene.h>


namespace diffCheck::geometry
{
    void DFMesh::Cvt2DFMesh(const std::shared_ptr<open3d::geometry::TriangleMesh> &O3DTriangleMesh)
    {
        this->Vertices.resize(O3DTriangleMesh->vertices_.size());
        for (size_t i = 0; i < O3DTriangleMesh->vertices_.size(); i++)
        {
            this->Vertices[i] = O3DTriangleMesh->vertices_[i];
        }

        this->Faces.resize(O3DTriangleMesh->triangles_.size());
        for (size_t i = 0; i < O3DTriangleMesh->triangles_.size(); i++)
        {
            this->Faces[i] = O3DTriangleMesh->triangles_[i];
        }
    }

    std::shared_ptr<open3d::geometry::TriangleMesh> DFMesh::Cvt2O3DTriangleMesh()
    {
        std::shared_ptr<open3d::geometry::TriangleMesh> O3DTriangleMesh = std::make_shared<open3d::geometry::TriangleMesh>();

        O3DTriangleMesh->vertices_.resize(this->Vertices.size());
        for (size_t i = 0; i < this->Vertices.size(); i++)
        {
            O3DTriangleMesh->vertices_[i] = this->Vertices[i];
        }

        O3DTriangleMesh->triangles_.resize(this->Faces.size());
        for (size_t i = 0; i < this->Faces.size(); i++)
        {
            O3DTriangleMesh->triangles_[i] = this->Faces[i];
        }

        O3DTriangleMesh->vertex_normals_.resize(this->NormalsVertex.size());
        for (size_t i = 0; i < this->NormalsVertex.size(); i++)
        {
            O3DTriangleMesh->vertex_normals_[i] = this->NormalsVertex[i];
        }

        O3DTriangleMesh->triangle_normals_.resize(this->NormalsFace.size());
        for (size_t i = 0; i < this->NormalsFace.size(); i++)
        {
            O3DTriangleMesh->triangle_normals_[i] = this->NormalsFace[i];
        }

        O3DTriangleMesh->vertex_colors_.resize(this->ColorsVertex.size());
        for (size_t i = 0; i < this->ColorsVertex.size(); i++)
        {
            O3DTriangleMesh->vertex_colors_[i] = this->ColorsVertex[i];
        }
        return O3DTriangleMesh;
    }

    std::shared_ptr<diffCheck::geometry::DFPointCloud> DFMesh::SampleCloudUniform(int numPoints)
    {
        auto O3DTriangleMesh = this->Cvt2O3DTriangleMesh();
        auto O3DPointCloud = O3DTriangleMesh->SamplePointsUniformly(numPoints);
        std::shared_ptr<geometry::DFPointCloud> DFPointCloud = std::make_shared<geometry::DFPointCloud>();
        DFPointCloud->Cvt2DFPointCloud(O3DPointCloud);
        return DFPointCloud;
    }

    void DFMesh::ApplyTransformation(const diffCheck::transformation::DFTransformation &transformation)
    {
        auto O3DTriangleMesh = this->Cvt2O3DTriangleMesh();
        O3DTriangleMesh->Transform(transformation.TransformationMatrix);
        this->Cvt2DFMesh(O3DTriangleMesh);
    }

    std::vector<Eigen::Vector3d> DFMesh::GetTightBoundingBox()
    {
        auto O3DTriangleMesh = this->Cvt2O3DTriangleMesh();
        open3d::geometry::OrientedBoundingBox tightOOBB = O3DTriangleMesh->GetMinimalOrientedBoundingBox();
        std::vector<Eigen::Vector3d> bboxPts = tightOOBB.GetBoxPoints();
        return bboxPts;
    }

    void DFMesh::LoadFromPLY(const std::string &path)
    {
        std::shared_ptr<diffCheck::geometry::DFMesh> tempMesh_ptr = diffCheck::io::ReadPLYMeshFromFile(path);
        this->Vertices = tempMesh_ptr->Vertices;
        this->Faces = tempMesh_ptr->Faces;
        this->NormalsVertex = tempMesh_ptr->NormalsVertex;
        this->ColorsVertex = tempMesh_ptr->ColorsVertex;
        this->NormalsFace = tempMesh_ptr->NormalsFace;
        this->ColorsFace = tempMesh_ptr->ColorsFace;
    }

    std::vector<float> DFMesh::ComputeDistance(const diffCheck::geometry::DFPointCloud &targetCloud, bool useAbs)
    {
        auto rayCastingScene = open3d::t::geometry::RaycastingScene();

        std::vector<Eigen::Vector3d> vertices = this->Vertices;
        std::vector<float> verticesPosition;
        for (const auto& vertex : vertices) {
            verticesPosition.insert(verticesPosition.end(), vertex.data(), vertex.data() + 3);
        }
        open3d::core::Tensor verticesPositionTensor(verticesPosition.data(), {static_cast<int64_t>(vertices.size()), 3}, open3d::core::Dtype::Float32);
        std::vector<uint32_t> triangles;
        for (int i = 0; i < this->Faces.size(); i++) {
            triangles.push_back(static_cast<uint32_t>(this->Faces[i].x()));
            triangles.push_back(static_cast<uint32_t>(this->Faces[i].y()));
            triangles.push_back(static_cast<uint32_t>(this->Faces[i].z()));
        }
        open3d::core::Tensor trianglesTensor(triangles.data(), {static_cast<int64_t>(this->Faces.size()), 3}, open3d::core::Dtype::UInt32);
        rayCastingScene.AddTriangles(verticesPositionTensor, trianglesTensor);

        auto pointCloudO3dCopy = targetCloud;
        std::shared_ptr<open3d::geometry::PointCloud> pointCloudO3d_ptr = pointCloudO3dCopy.Cvt2O3DPointCloud();
        std::vector<float> cloudPoints;
        for (const auto& point : pointCloudO3d_ptr->points_) {
            cloudPoints.insert(cloudPoints.end(), point.data(), point.data() + 3);
        }
        open3d::core::Tensor cloudPointsTensor(cloudPoints.data(), {static_cast<int64_t>(pointCloudO3d_ptr->points_.size()), 3}, open3d::core::Dtype::Float32);

        open3d::core::Tensor sdf = rayCastingScene.ComputeSignedDistance(cloudPointsTensor);
        if (useAbs)
            sdf = sdf.Abs();
        std::vector<float> sdfVector(sdf.GetDataPtr<float>(), sdf.GetDataPtr<float>() + sdf.NumElements());

        return sdfVector;
    }
} // namespace diffCheck::geometry