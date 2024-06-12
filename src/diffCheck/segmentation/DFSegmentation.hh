#pragma once
#include "diffCheck.hh"

namespace diffCheck::segmentation
{
    class DFSegmentation
    {
        public:
        /** @brief Segment the point cloud into planes
         * Using Cilantro's ConnectedComponentExtraction3f method
         * @param pointCloud the point cloud to segment
         * @param voxelSize the voxel size for the search in the point cloud
         * @param normalThresholdDegree the normal threshold in degrees do differentiate segments
         * @param minClusterSize the minimum cluster size to consider a segment
         * @return std::vector<geometry::DFPointCloud> the segmented point clouds
         */
        static std::vector<std::shared_ptr<geometry::DFPointCloud>> SegmentationPointCloud(
            geometry::DFPointCloud &pointCloud,
            float voxelSize = 0.2,
            float normalThresholdDegree = 20,
            int minClusterSize = 10);    
    };
} // namespace diffCheck::segmentation