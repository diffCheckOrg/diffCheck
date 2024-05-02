#pragma once
# include "diffCheck.hh"

# include <open3d/pipelines/registration/Registration.h>

namespace diffCheck::registration
{
    class RefinedRegistration
    {
        public: ///< open3d registration methods
        /**
         * @brief Perform ICP registration using Open3D
         * 
         * @param source DFPointCloud source point cloud
         * @param target DFPointCloud Target point cloud
         * @param maxCorrespondenceDistance Maximum relative correspondence distance. 0.01 means 1% of the bounding box diagonal
         * @return diffCheck::transformation::DFTransformation
        */
        static diffCheck::transformation::DFTransformation O3DICP(
            std::shared_ptr<geometry::DFPointCloud> source, 
            std::shared_ptr<geometry::DFPointCloud> target,
            double maxCorrespondenceDistance = 0.01);

        /**
         * @brief Perform Generalized ICP registration using Open3D
         * 
         * @param source DFPointCloud source point cloud
         * @param target DFPointCloud Target point cloud
         * @param maxCorrespondenceDistance Maximum relative correspondence distance. 0.01 means 1% of the bounding box diagonal
         * @return diffCheck::transformation::DFTransformation
         */
        static diffCheck::transformation::DFTransformation O3DGeneralizedICP(
            std::shared_ptr<geometry::DFPointCloud> source, 
            std::shared_ptr<geometry::DFPointCloud> target,
            double maxCorrespondenceDistance = 0.01);
    };
}