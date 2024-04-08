#pragma once

#include "diffCheck.hh"
#include <open3d/pipelines/registration/Registration.h>

namespace diffCheck::registration{

class Registration
{
    public:
    
    std::vector<double> ComputeP2PDistance(std::shared_ptr<geometry::DFPointCloud> source, std::shared_ptr<geometry::DFPointCloud> target);
    
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
    open3d::pipelines::registration::RegistrationResult O3DFastGlobalRegistrationFeatureMatching(std::shared_ptr<geometry::DFPointCloud> source, std::shared_ptr<geometry::DFPointCloud> target);

    /*
    Very little information on this registration method compared to the previous one.
    If I understand correctly, this method finds keypoints in the FPFH hyperspaces of the source and target point clouds and then tries to match them.
    https://pcl.readthedocs.io/projects/tutorials/en/latest/correspondence_grouping.html 
    */ 
    open3d::pipelines::registration::RegistrationResult O3DFastGlobalRegistrationBasedOnCorrespondence(std::shared_ptr<geometry::DFPointCloud> source, std::shared_ptr<geometry::DFPointCloud> target);
    /*
    Ransac registration based on correspondence:
    Correspondances are computed between the source and target point clouds.
    Then, a transformation is computed that minimizes the error between the correspondances. 
    If the error is above a certain threshold, the transformation is discarded and a new one is computed.

    In practice, Open3D gives little information about the feature correspondence

    */
    open3d::pipelines::registration::RegistrationResult Registration::O3DRansacOnCorrespondence(std::shared_ptr<geometry::DFPointCloud> source, std::shared_ptr<geometry::DFPointCloud> target);
    /*
    Ransac registration based on Feature Matching
    https://www.open3d.org/docs/release/tutorial/pipelines/global_registration.html#RANSAC
    */
    open3d::pipelines::registration::RegistrationResult Registration::O3DRansacOnFeatureMatching(std::shared_ptr<geometry::DFPointCloud> source, std::shared_ptr<geometry::DFPointCloud> target);

    

    
};
}