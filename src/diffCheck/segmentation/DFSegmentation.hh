#pragma once
#include "diffCheck.hh"

namespace diffCheck::segmentation
{
    class DFSegmentation
    {
        public:
        /** @brief Downsamples and segments the point cloud using Cilantro's ConnectedComponentExtraction3f method. It uses the normals' variations to detect different parts in the point cloud.
         * @param pointCloud the point cloud to segment
         * @param voxelSize the voxel size for the downsampling of the point cloud. The point cloud is downsampled after the normal calculation. A lower number will result in a denser point cloud
         * @param normalThresholdDegree the normal threshold in degrees do differentiate segments. The higher the number, the more tolerent the segmentation will be to normal differences
         * @param minClusterSize the minimum cluster size to consider a segment. A lower number will discard smaller segments
         * @param useKnnNeighborhood if true, the neighborhood search will be done using the knnNeighborhoodSize, otherwise it will be done using radiusNeighborhoodSize
         * @param knnNeighborhoodSize the k nearest neighbors size for the "neighborhood search". This is used when useKnnNeighborhood is true. a higher number will result in smoother segmentation, but at the cost of computation time
         * @param radiusNeighborhoodSize the radius of the neighborhood size for the "radius search". This is used when useKnnNeighborhood is false. A higher number will result in smoother segmentation, but at the cost of computation time.
         * @return std::vector<std::shared_ptr<geometry::DFPointCloud>> the segmented point clouds
         */
        static std::vector<std::shared_ptr<geometry::DFPointCloud>> NormalBasedSegmentation(
            geometry::DFPointCloud &pointCloud,
            float voxelSize = 0.2,
            float normalThresholdDegree = 20,
            int minClusterSize = 10,
            bool useKnnNeighborhood = true,
            int knnNeighborhoodSize = 10,
            int radiusNeighborhoodSize = 10);
        
        /**
         * @brief From a vector of mesh faces, finds in a vector of cloud segments the corresponding segments as a unified point cloud
         * @param meshFaces the mesh faces to compare
         * @param segments the segments to compare
         * @return std::tuple<std::shared_ptr<geometry::DFPointCloud>, std::vector<std::shared_ptr<geometry::DFPointCloud>> > the unified point cloud and the corresponding segments as a tuple
        */
        static std::tuple<std::shared_ptr<geometry::DFPointCloud>, std::vector<std::shared_ptr<geometry::DFPointCloud>>> AssociateSegments(
            std::vector<std::shared_ptr<geometry::DFMesh>> meshFaces,
            std::vector<std::shared_ptr<geometry::DFPointCloud>> segments,
            double associationThreshold);
    };
} // namespace diffCheck::segmentation