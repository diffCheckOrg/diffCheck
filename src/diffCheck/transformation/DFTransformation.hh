#pragma once
#include <Eigen/Core>

namespace diffCheck::transformation
{
    class DFTransformation
    {
    public:
        /**
         * @brief 4x4 Transformation matrix for point clouds
         */
        Eigen::Matrix4d transformationMatrix;

        /**
         * @brief 3x3 Rotation matrix for point clouds 
         */
        Eigen::Matrix3d rotationMatrix;

        /**
         * @brief 3x1 Translation vector for point clouds
         */
        Eigen::Vector3d translationVector;

    };  
}