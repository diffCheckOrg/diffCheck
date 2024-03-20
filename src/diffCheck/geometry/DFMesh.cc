#include "diffCheck/geometry/DFMesh.hh"

#include "diffCheck/IOManager.hh"


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

        this->NormalsVertex.resize(O3DTriangleMesh->vertex_normals_.size());
        for (size_t i = 0; i < O3DTriangleMesh->vertex_normals_.size(); i++)
        {
            this->NormalsVertex[i] = O3DTriangleMesh->vertex_normals_[i];
        }

        this->NormalsFace.resize(O3DTriangleMesh->triangle_normals_.size());
        for (size_t i = 0; i < O3DTriangleMesh->triangle_normals_.size(); i++)
        {
            this->NormalsFace[i] = O3DTriangleMesh->triangle_normals_[i];
        }

        this->ColorsVertex.resize(O3DTriangleMesh->vertex_colors_.size());
        for (size_t i = 0; i < O3DTriangleMesh->vertex_colors_.size(); i++)
        {
            this->ColorsVertex[i] = O3DTriangleMesh->vertex_colors_[i];
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

    void DFMesh::LoadFromPLY(const std::string &path)
    {
        diffCheck::io::ReadPLYMeshFromFile(path);
        this->Vertices = diffCheck::io::ReadPLYMeshFromFile(path)->Vertices;
        this->Faces = diffCheck::io::ReadPLYMeshFromFile(path)->Faces;
        this->NormalsVertex = diffCheck::io::ReadPLYMeshFromFile(path)->NormalsVertex;
        this->ColorsVertex = diffCheck::io::ReadPLYMeshFromFile(path)->ColorsVertex;
        this->NormalsFace = diffCheck::io::ReadPLYMeshFromFile(path)->NormalsFace;
        this->ColorsFace = diffCheck::io::ReadPLYMeshFromFile(path)->ColorsFace;
    }
} // namespace diffCheck::geometry