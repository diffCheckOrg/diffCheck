#include "Registration.hh"

namespace diffCheck::registration
{
    void Registration::RegisterICPO3D( std::shared_ptr<diffCheck::geometry::DFPointCloud> &source, std::shared_ptr<diffCheck::geometry::DFPointCloud> &target, double threshold)
    {
        // Convert the source and target point clouds to open3d point clouds
        std::cout<<"pop1"<<std::endl;
        std::shared_ptr<open3d::geometry::PointCloud> sourceO3D = source->Cvt2O3DPointCloud();
        std::shared_ptr<open3d::geometry::PointCloud> targetO3D = target->Cvt2O3DPointCloud();
        std::cout<<"pop1.1"<<std::endl;
        // Perform the ICP registration
        auto result = open3d::pipelines::registration::RegistrationICP(*sourceO3D, *targetO3D, threshold, Eigen::Matrix4d::Identity(), open3d::pipelines::registration::TransformationEstimationPointToPoint());
        std::cout<<"pop1.2"<<std::endl;
        sourceO3D->Transform(result.transformation_);
        // Convert the result to our point cloud format
        source->Cvt2DFPointCloud(sourceO3D);
    }

    void Registration::PopulateMesh( std::shared_ptr<diffCheck::geometry::DFMesh> &mesh, std::shared_ptr<diffCheck::geometry::DFPointCloud> &pointCloud, int numPoints)
    {
        // Convert the point cloud to open3d point cloud
        std::shared_ptr<open3d::geometry::TriangleMesh> meshO3D = std::make_shared<open3d::geometry::TriangleMesh>();
        // Convert the mesh to open3d mesh
        meshO3D = mesh->Cvt2O3DTriangleMesh();

        std::cout << " Number of vertices in the mesh: " << meshO3D->vertices_.size() << std::endl;
        std::cout << " Number of triangles in the mesh: " << meshO3D->triangles_.size() << std::endl;
        std::cout << " Number of triangle normals in the mesh: " << meshO3D->triangle_normals_.size() << std::endl;
        std::cout << " Number of vertex normals in the mesh: " << meshO3D->vertex_normals_.size() << std::endl;
        // Populate the mesh with the point cloud and store the result behind diffCheck PointCloud pointer
        std::shared_ptr<open3d::geometry::PointCloud> pointCloudO3D = meshO3D->SamplePointsUniformly(numPoints);
        std::cout<<"pop1.3"<<std::endl;
        pointCloud->Cvt2DFPointCloud(pointCloudO3D);
    }
}