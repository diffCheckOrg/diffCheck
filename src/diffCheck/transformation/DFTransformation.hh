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
        DFTransformation(const Eigen::Matrix3d& rotationMatrix, const Eigen::Vector3d& translationVector) 
            : RotationMatrix(rotationMatrix), TranslationVector(translationVector)
        {}

    public:
        /**
         * @brief 4x4 Transformation matrix for point clouds
         */
        Eigen::Matrix4d TransformationMatrix;

        /**
         * @brief 3x3 Rotation matrix for point clouds 
         */
        Eigen::Matrix3d RotationMatrix;

        /**
         * @brief 3x1 Translation vector for point clouds
         */
        Eigen::Vector3d TranslationVector;
    };
}