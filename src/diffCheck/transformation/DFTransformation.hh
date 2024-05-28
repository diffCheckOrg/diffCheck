#pragma once
#include <Eigen/Core>

namespace diffCheck::transformation
{
    class DFTransformation
    {
    public:
        DFTransformation() = default;
        DFTransformation(const Eigen::Matrix4d& transformationMatrix)
            : TransformationMatrix(transformationMatrix)
        {}

    public:
        /**
         * @brief 4x4 Transformation matrix for point clouds
         */
        Eigen::Matrix4d TransformationMatrix;
    };
}