#include "DFRefinedRegistration.hh"


namespace diffCheck::registration
{
    diffCheck::transformation::DFTransformation RefinedRegistration::O3DICP(
        std::shared_ptr<geometry::DFPointCloud> source, 
        std::shared_ptr<geometry::DFPointCloud> target,
        double maxCorrespondenceDistance,
        bool scalingForPointToPointTransformationEstimation,
        double relativeFitness,
        double relativeRMSE,
        int maxIteration,
        bool usePointToPlane)
    {
        std::vector<Eigen::Vector3d> minMax = source->ComputeBoundingBox();
        double scale = (minMax[1] - minMax[0]).norm();
        double absoluteMaxCorrespondenceDistance = maxCorrespondenceDistance * scale;

        std::shared_ptr<open3d::geometry::PointCloud> O3Dsource = source->Cvt2O3DPointCloud();
        std::shared_ptr<open3d::geometry::PointCloud> O3Dtarget = target->Cvt2O3DPointCloud();
        Eigen::Matrix4d initialTransformation = Eigen::Matrix4d::Identity();
        open3d::pipelines::registration::ICPConvergenceCriteria criteria
            = open3d::pipelines::registration::ICPConvergenceCriteria(
                relativeFitness, 
                relativeRMSE,
                maxIteration);

        open3d::pipelines::registration::RegistrationResult result;

        if(usePointToPlane)
        {
            O3Dsource->EstimateNormals();
            O3Dtarget->EstimateNormals();
            open3d::pipelines::registration::TransformationEstimationPointToPlane transformation_estimation 
                = open3d::pipelines::registration::TransformationEstimationPointToPlane();
            result = open3d::pipelines::registration::RegistrationICP(
                *O3Dsource, 
                *O3Dtarget, 
                absoluteMaxCorrespondenceDistance,
                initialTransformation,
                transformation_estimation,
                criteria);
        }
        else
        {
            open3d::pipelines::registration::TransformationEstimationPointToPoint transformation_estimation 
                = open3d::pipelines::registration::TransformationEstimationPointToPoint(scalingForPointToPointTransformationEstimation);
            result = open3d::pipelines::registration::RegistrationICP(
                *O3Dsource, 
                *O3Dtarget, 
                absoluteMaxCorrespondenceDistance,
                initialTransformation,
                transformation_estimation,
                criteria);
        }
        
        diffCheck::transformation::DFTransformation transformation 
            = diffCheck::transformation::DFTransformation(result.transformation_);
        return transformation;
    }
    diffCheck::transformation::DFTransformation RefinedRegistration::O3DGeneralizedICP(
        std::shared_ptr<geometry::DFPointCloud> source,
        std::shared_ptr<geometry::DFPointCloud> target,
         double maxCorrespondenceDistance,
            int maxIteration,
            double relativeFitness,
            double relativeRMSE)
    {
        std::vector<Eigen::Vector3d> minMax = source->ComputeBoundingBox();
        double scale = (minMax[1] - minMax[0]).norm();
        double absoluteMaxCorrespondenceDistance = maxCorrespondenceDistance * scale;

        std::shared_ptr<open3d::geometry::PointCloud> O3Dsource = source->Cvt2O3DPointCloud();
        std::shared_ptr<open3d::geometry::PointCloud> O3Dtarget = target->Cvt2O3DPointCloud();

        O3Dsource->EstimateCovariances();
        O3Dtarget->EstimateCovariances();

        Eigen::Matrix4d initialTransformation = Eigen::Matrix4d::Identity();
        open3d::pipelines::registration::ICPConvergenceCriteria criteria
            = open3d::pipelines::registration::ICPConvergenceCriteria(
                relativeFitness, 
                relativeRMSE,
                maxIteration);

        open3d::pipelines::registration::TransformationEstimationForGeneralizedICP transformation_estimation 
            = open3d::pipelines::registration::TransformationEstimationForGeneralizedICP();

        open3d::pipelines::registration::RegistrationResult result 
            = open3d::pipelines::registration::RegistrationGeneralizedICP(
                *O3Dsource, 
                *O3Dtarget, 
                absoluteMaxCorrespondenceDistance,
                initialTransformation,
                transformation_estimation,
                criteria);

        diffCheck::transformation::DFTransformation transformation 
            = diffCheck::transformation::DFTransformation(result.transformation_);
        return transformation;
    }
}