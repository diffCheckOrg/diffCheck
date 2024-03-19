#include "IOManager.hh"

#include <igl/readPLY.h>



namespace diffCheck::io
{
    // TODO: return a dggeometry::Mesh object
    void ReadPLYMeshFromFile(const std::string &filename)
    {
        Eigen::MatrixXd V;
        Eigen::MatrixXi F;
        igl::readPLY(filename, V, F);
    }

    std::shared_ptr<diffCheck::geometry::DFPointCloud> ReadPLYPointCloud(const std::string &filename)
    {
        std::shared_ptr<diffCheck::geometry::DFPointCloud> pointCloud = std::make_shared<diffCheck::geometry::DFPointCloud>();
        Eigen::MatrixXd V;
        Eigen::MatrixXd C;
        Eigen::MatrixXd N;
        Eigen::MatrixXi F;
        
        igl::readPLY(filename, V, F, C, N);

        pointCloud->Points.resize(V.rows());
        for (int i = 0; i < V.rows(); i++)
        {
            pointCloud->Points[i] = V.row(i);
        }
        pointCloud->Colors.resize(C.rows());
        for (int i = 0; i < C.rows(); i++)
        {
            pointCloud->Colors[i] = C.row(i);
        }
        pointCloud->Normals.resize(N.rows());
        for (int i = 0; i < N.rows(); i++)
        {
            pointCloud->Normals[i] = N.row(i);
        }
        return pointCloud;
    }
} // namespace diffCheck::io