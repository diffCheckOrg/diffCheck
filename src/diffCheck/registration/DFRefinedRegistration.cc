#include "refinedRegistration.hh"


namespace diffCheck::registration
{
    open3d::pipelines::registration::RegistrationResult RefinedRegistration::O3DICP(
        std::shared_ptr<geometry::DFPointCloud> source, 
        std::shared_ptr<geometry::DFPointCloud> target,
        double maxCorrespondenceDistance)
    {
        std::shared_ptr<open3d::geometry::PointCloud> O3Dsource = source->Cvt2O3DPointCloud();
        std::shared_ptr<open3d::geometry::PointCloud> O3Dtarget = target->Cvt2O3DPointCloud();
        open3d::pipelines::registration::RegistrationResult result = open3d::pipelines::registration::RegistrationICP(
            *O3Dsource, 
            *O3Dtarget, 
            maxCorrespondenceDistance);
        return result;
    }
    open3d::pipelines::registration::RegistrationResult RefinedRegistration::O3DGeneralizedICP(
        std::shared_ptr<geometry::DFPointCloud> source, 
        std::shared_ptr<geometry::DFPointCloud> target,
        double maxCorrespondenceDistance)
    {
        std::shared_ptr<open3d::geometry::PointCloud> O3Dsource = source->Cvt2O3DPointCloud();
        std::shared_ptr<open3d::geometry::PointCloud> O3Dtarget = target->Cvt2O3DPointCloud();
        open3d::pipelines::registration::RegistrationResult result = open3d::pipelines::registration::RegistrationICP(
            *O3Dsource, 
            *O3Dtarget, 
            maxCorrespondenceDistance);
        return result;
    }
}