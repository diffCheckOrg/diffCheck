#include "registration.hh"

namespace diffCheck::registration
{
    std::vector<double> Registration::ComputeP2PDistance(std::shared_ptr<geometry::DFPointCloud> source, std::shared_ptr<geometry::DFPointCloud> target)
    {
        std::vector<double> errors;
        auto O3DSourcePointCloud = source->Cvt2O3DPointCloud();
        auto O3DTargetPointCloud = target->Cvt2O3DPointCloud();
        
        std::vector<double> distances;

        distances = O3DSourcePointCloud->ComputePointCloudDistance(*O3DTargetPointCloud);
        return distances;
    }
    /*
    Documentation on Fast Point Feature Historigrams: https://pcl.readthedocs.io/projects/tutorials/en/latest/fpfh_estimation.html
    
    Very simply, point features are values computed on a point cloud (for example the normal of a point, the curvature, etc.).
    point features historigrams generalize this concept by computing point features in a local neighborhood of a point, stored as higher-dimentional historigrams.

    For example, for a given point, you take all the neighboring points within a given radius, and create a complete graph on those vertices.
    then for each edge of the graph you compute features that are then stored in a historigram of the original center point from which the sphere and the graph where built.
    https://pcl.readthedocs.io/projects/tutorials/en/latest/pfh_estimation.html#pfh-estimation proposes a simple example of such a historigram.

    PCL's documentation refers to this 2009 TUM PhD thesis (but largely outside the scope of our work): https://mediatum.ub.tum.de/doc/800632/941254.pdf

    Quite important for us: the resultant hyperspace is dependent on the quality of the surface normal estimations at each point (if pc noisy, historigram different).
    */
    open3d::pipelines::registration::RegistrationResult Registration::O3DFastGlobalRegistrationFeatureMatching(std::shared_ptr<geometry::DFPointCloud> source, std::shared_ptr<geometry::DFPointCloud> target)
        {
        std::shared_ptr<open3d::geometry::PointCloud> sourceO3D = source->Cvt2O3DPointCloud();
        std::shared_ptr<open3d::geometry::PointCloud> targetO3D = target->Cvt2O3DPointCloud();

        sourceO3D->RandomDownSample(0.1);
        targetO3D->RandomDownSample(0.1);

        std::shared_ptr<open3d::pipelines::registration::Feature> sourceFPFHFeatures = open3d::pipelines::registration::ComputeFPFHFeature(*sourceO3D,
                                                                                                                                           open3d::geometry::KDTreeSearchParamHybrid(0.25, 30));
        std::shared_ptr<open3d::pipelines::registration::Feature> targetFPFHFeatures = open3d::pipelines::registration::ComputeFPFHFeature(*targetO3D,
                                                                                                                                           open3d::geometry::KDTreeSearchParamHybrid(0.25, 30));
        std::shared_ptr<open3d::pipelines::registration::FastGlobalRegistrationOption> option = std::make_shared<open3d::pipelines::registration::FastGlobalRegistrationOption>();
        option->maximum_correspondence_distance_ = 0.05;
        option->iteration_number_ = 100;
        option->maximum_tuple_count_ = 500;

        auto result = open3d::pipelines::registration::FastGlobalRegistrationBasedOnFeatureMatching(*sourceO3D,
                                                                                                    *targetO3D,
                                                                                                    *sourceFPFHFeatures,
                                                                                                    *targetFPFHFeatures,
                                                                                                    *option);

        return result;
    }
    /*
    Very little information on this registration method compared to the previous one.
    If I understand correctly, this method finds keypoints in the FPFH hyperspaces of the source and target point clouds and then tries to match them.
    https://pcl.readthedocs.io/projects/tutorials/en/latest/correspondence_grouping.html 
    */
    open3d::pipelines::registration::RegistrationResult Registration::O3DFastGlobalRegistrationBasedOnCorrespondence(std::shared_ptr<geometry::DFPointCloud> source, std::shared_ptr<geometry::DFPointCloud> target)
    {
        std::shared_ptr<open3d::geometry::PointCloud> sourceO3D = source->Cvt2O3DPointCloud();
        std::shared_ptr<open3d::geometry::PointCloud> targetO3D = target->Cvt2O3DPointCloud();

        sourceO3D->RandomDownSample(0.1);
        targetO3D->RandomDownSample(0.1);

        std::shared_ptr<open3d::pipelines::registration::FastGlobalRegistrationOption> option = std::make_shared<open3d::pipelines::registration::FastGlobalRegistrationOption>();
        option->maximum_correspondence_distance_ = 0.05;
        option->iteration_number_ = 100;
        option->maximum_tuple_count_ = 500;

        std::shared_ptr<open3d::pipelines::registration::Feature> sourceFPFHFeatures = open3d::pipelines::registration::ComputeFPFHFeature(*sourceO3D,
                                                                                                                                           open3d::geometry::KDTreeSearchParamHybrid(0.25, 30));
        std::shared_ptr<open3d::pipelines::registration::Feature> targetFPFHFeatures = open3d::pipelines::registration::ComputeFPFHFeature(*targetO3D,
                                                                                                                                           open3d::geometry::KDTreeSearchParamHybrid(0.25, 30));
        

        open3d::pipelines::registration::CorrespondenceSet correspondanceset;
        correspondanceset = open3d::pipelines::registration::CorrespondencesFromFeatures(*sourceFPFHFeatures, *targetFPFHFeatures);

        auto result = open3d::pipelines::registration::FastGlobalRegistrationBasedOnCorrespondence(*sourceO3D,
                                                                                                    *targetO3D,
                                                                                                    correspondanceset,
                                                                                                    *option);
        return result;
    }
} 