#include "visualizer.hh"


namespace diffCheck::visualizer
{
    void Visualizer::LoadPointCloud(std::shared_ptr<diffCheck::geometry::DFPointCloud> &pointCloud)
    {
        Eigen::MatrixXd V(pointCloud->Points.size(), 3);
        for (int i = 0; i < pointCloud->Points.size(); i++)
        {
            V(i, 0) = pointCloud->Points[i](0);
            V(i, 1) = pointCloud->Points[i](1);
            V(i, 2) = pointCloud->Points[i](2);
        }
        Eigen::MatrixXd C(pointCloud->Colors.size(), 3);
        for (int i = 0; i < pointCloud->Colors.size(); i++)
        {
            C(i, 0) = pointCloud->Colors[i](0);
            C(i, 1) = pointCloud->Colors[i](1);
            C(i, 2) = pointCloud->Colors[i](2);
        }
        this->m_Viewer.data().set_points(V, C);
        this->m_Viewer.data().point_size = 10;
    }

    void Visualizer::LoadMesh(std::shared_ptr<diffCheck::geometry::DFMesh> &mesh)
    {
        Eigen::MatrixXd V(mesh->Vertices.size(), 3);
        for (int i = 0; i < mesh->Vertices.size(); i++)
        {
            V(i, 0) = mesh->Vertices[i](0);
            V(i, 1) = mesh->Vertices[i](1);
            V(i, 2) = mesh->Vertices[i](2);
        }
        Eigen::MatrixXi F(mesh->Faces.size(), 3);
        for (int i = 0; i < mesh->Faces.size(); i++)
        {
            F(i, 0) = mesh->Faces[i](0);
            F(i, 1) = mesh->Faces[i](1);
            F(i, 2) = mesh->Faces[i](2);
        }
        this->m_Viewer.data().set_mesh(V, F);
    }

    void Visualizer::Run()
    {
        this->m_Viewer.launch(
            false,                   // fullscreen
            "DiffCheck",             // window title
            1280,                    // window width
            720);                    // window height
    }
} // namespace diffCheck::visualizer