# State of the art relevant for diffCheck

## Open3d 0.17.0
the open3d::pipelines::registration namespace provides different tools for registration.

Registration methods:
- ```FastGlobalRegistrationBasedOnCorrespondence()```
- ```FastGlobalRegistrationBasedOnFeatureMatching()```
- ```RegistrationColoredICP()``` (from https://doi.org/10.1109/ICCV.2017.25 )
Does NOT use 6d points registration (xyzrgb) but makes a first ICP registration based on xyz, then for each point creates a virtual image taken towards this point and along its normal, with intensities instead of rgb. If I understand correctly, they compute the error between the target point's image and the source point's image and compute the refinement transformation to minimize this error. The virtual image is simplified by using the point's intensity and for the virtual pixels next to it approgimating them by the value of the centerpoint + gradient*distance.
- ```GlobalOptimization()``` (from https://doi.org/10.1109/CVPR.2015.7299195 )
- ```RegistrationGeneralizedICP()``` (from http://dx.doi.org/10.15607/RSS.2009.V.021)
combines traditional ICP with "point-to-plane" ICP. Point to plane ICP identifies planes in the target point cloud and minimizes the distance between the source point cloud and the target planes, by using the normals of the target and performing the scalar product.

- ```RegistrationICP()```
- ```RegistrationRANSACBasedOnCorrespondence()```
- ```RegistrationRANSACBasedOnFeatureMatching()```

## Nice papers