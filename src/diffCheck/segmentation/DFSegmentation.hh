#pragma once
#include "diffCheck.hh"

namespace diffCheck::segmentation
{
    class DFSegmentation
    {
        public:
        /** @brief Downsamples and segments the point cloud using Cilantro's ConnectedComponentExtraction3f method. It uses the normals' variations to detect different parts in the point cloud.
         * @param pointCloud the point cloud to segment
         * @param normalThresholdDegree the normal threshold in degrees do differentiate segments. The higher the number, the more tolerent the segmentation will be to normal differences
         * @param minClusterSize the minimum cluster size to consider a segment. A lower number will discard smaller segments
         * @param useKnnNeighborhood if true, the neighborhood search will be done using the knnNeighborhoodSize, otherwise it will be done using radiusNeighborhoodSize
         * @param knnNeighborhoodSize the k nearest neighbors size for the "neighborhood search". This is used when useKnnNeighborhood is true. a higher number will result in smoother segmentation, but at the cost of computation time
         * @param radiusNeighborhoodSize the radius of the neighborhood size for the "radius search". This is used when useKnnNeighborhood is false. A higher number will result in smoother segmentation, but at the cost of computation time.
         * @param colorClusters if true, the clusters will be colored with random colors
         * @return std::vector<std::shared_ptr<geometry::DFPointCloud>> the segmented point clouds
         */
        static std::vector<std::shared_ptr<geometry::DFPointCloud>> NormalBasedSegmentation(
            std::shared_ptr<geometry::DFPointCloud> &pointCloud,
            float normalThresholdDegree = 20.f,
            int minClusterSize = 10,
            bool useKnnNeighborhood = true,
            int knnNeighborhoodSize = 10,
            float radiusNeighborhoodSize = 10.f,
            bool colorClusters = false);
    };
} // namespace diffCheck::segmentation