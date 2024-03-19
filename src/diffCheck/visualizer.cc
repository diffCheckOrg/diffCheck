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

    // TODO: implement the  diffCHeck mesh object
    void Visualizer::LoadMesh(const Eigen::MatrixXd &V, const Eigen::MatrixXi &F)
    {
        this->m_Viewer.data().set_mesh(V, F);
        this->m_Viewer.data().set_face_based(true);
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