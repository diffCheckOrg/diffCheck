#pragma once

#include <open3d/Open3D.h>
#include <loguru.hpp>

#include <cilantro/cilantro.hpp>

// diffCheck includes
#include "diffCheck/log.hh"
const diffCheck::Log LOG = diffCheck::Log();

#include "diffCheck/geometry/DFPointCloud.hh"
#include "diffCheck/geometry/DFMesh.hh"
#include "diffCheck/IOManager.hh"
#include "diffCheck/visualizer.hh"
#include "diffCheck/transformation/DFTransformation.hh"
#include "diffCheck/registrations/DFGlobalRegistrations.hh"
#include "diffCheck/registrations/DFRefinedRegistration.hh"
#include "diffCheck/segmentation/DFSegmentation.hh"
