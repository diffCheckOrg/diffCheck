#pragma once

#include <open3d/Open3D.h>
#include <loguru.hpp>

// diffCheck includes
#include "diffCheck/log.hh"
const diffCheck::Log LOG = diffCheck::Log();

#include "diffCheck/geometry/DFPointCloud.hh"
#include "diffCheck/geometry/DFMesh.hh"
#include "diffCheck/IOManager.hh"
#include "diffCheck/visualizer.hh"