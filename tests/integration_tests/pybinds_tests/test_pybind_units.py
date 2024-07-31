import pytest
import os
import sys


# Import the C++ bindings
extra_dll_dir = os.path.join(os.path.dirname(__file__), "./")
os.add_dll_directory(extra_dll_dir)  # For finding DLL dependencies on Windows
sys.path.append(extra_dll_dir)  # Add this directory to the Python path
try:
    import diffcheck_bindings as dfb
except ImportError as e:
    print(f"Failed to import diffcheck_bindings: {e}")
    print("Current sys.path directories:")
    for path in sys.path:
        print(path)
    print("Current files in the directory:")
    for file in os.listdir(extra_dll_dir):
        print(file)
    sys.exit(1)

def get_ply_cloud_roof_quarter_path():
    base_test_data_dir = os.getenv('DF_TEST_DATA_DIR', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'test_data')))
    ply_file_path = os.path.join(base_test_data_dir, "roof_quarter.ply")
    if not os.path.exists(ply_file_path):
        raise FileNotFoundError(f"PLY file not found at: {ply_file_path}")
    print(f"base_test_data_dir: {base_test_data_dir}")  #TODO: Debug
    print(f"ply_file_path: {ply_file_path}")  #TODO: Debug
    return ply_file_path

#------------------------------------------------------------------------------
# dfb_geometry namespace
#------------------------------------------------------------------------------

def test_DFPointCloud_init():
    # Assuming Eigen::Vector3d maps to a tuple of 3 floats in Python
    points = [(1.0, 2.0, 3.0), (4.0, 5.0, 6.0), (7.0, 8.0, 9.0)]
    normals = [(0.1, 0.2, 0.3), (0.4, 0.5, 0.6), (0.7, 0.8, 0.9)]
    colors = [(10, 20, 30), (40, 50, 60), (70, 80, 90)]

    pc = dfb.dfb_geometry.DFPointCloud(points, normals, colors)
    assert pc is not None, "DFPointCloud should be initialized successfully"

def test_DFPointCloud_load_from_PLY():
    pc = dfb.dfb_geometry.DFPointCloud()
    pc.load_from_PLY(get_ply_cloud_roof_quarter_path())
    
    assert pc.points.__len__() == 7379, "DFPointCloud should have 7379 points"
    assert pc.normals.__len__() == 7379, "DFPointCloud should have 7379 normals"
    assert pc.colors.__len__() == 7379, "DFPointCloud should have 7379 colors"

@pytest.fixture
def create_DFPointCloudSampleRoof():
    df_pcd = dfb.dfb_geometry.DFPointCloud()
    df_pcd.load_from_PLY(get_ply_cloud_roof_quarter_path())
    yield df_pcd

def test_DFPointCloud_properties(create_DFPointCloudSampleRoof):
    pc = create_DFPointCloudSampleRoof
    assert pc.points.__len__() == 7379, "DFPointCloud should have 7379 points"
    assert pc.normals.__len__() == 7379, "DFPointCloud should have 7379 normals"
    assert pc.colors.__len__() == 7379, "DFPointCloud should have 7379 colors"

    assert pc.get_num_points() == 7379, "get_num_points() should return 7379"
    assert pc.get_num_normals() == 7379, "get_num_normals() should return 7379"
    assert pc.get_num_colors() == 7379, "get_num_colors() should return 7379"

    assert pc.has_points() == True, "has_points() should return True"
    assert pc.has_colors() == True, "has_colors() should return True"
    assert pc.has_normals() == True, "has_normals() should return True"

    pc.points = []
    pc.normals = []
    pc.colors = []
    assert pc.has_points() == False, "has_points() should return False"
    assert pc.has_colors() == False, "has_colors() should return False"
    assert pc.has_normals() == False, "has_normals() should return False"

def test_DFPointCloud_apply_color(create_DFPointCloudSampleRoof):
    pc = create_DFPointCloudSampleRoof
    pc.apply_color(255, 0, 0)
    for color in pc.colors:
        assert (color[0] == 1 and color[1] == 0 and color[2] == 0), "All colors should be (255, 0, 0)"

def test_DFPointCloud_voxel_func(create_DFPointCloudSampleRoof):
    pc = create_DFPointCloudSampleRoof
    pc.voxel_downsample(0.01)
    assert pc.points.__len__() == 7256, "DFPointCloud should have 7256 points"
    pc.uniform_downsample(3)
    assert pc.points.__len__() == 2419, "DFPointCloud should have 2419 points"
    pc.downsample_by_size(1000)
    assert pc.points.__len__() == 1000, "DFPointCloud should have 1000 points"

def test_DFPointCloud_compute_normals(create_DFPointCloudSampleRoof):
    pc = create_DFPointCloudSampleRoof
    pc.normals.clear()
    pc.estimate_normals()
    assert pc.normals.__len__() == 7379, "DFPointCloud should have 7379 normals"

def test_DFPointCloud_get_tight_bounding_box(create_DFPointCloudSampleRoof):
    pc = create_DFPointCloudSampleRoof
    obb = pc.get_tight_bounding_box()
    assert obb[0][0] == 0.1955558282162114, "The min x of the OBB should be 0.1955558282162114"

# TODO: to implement DFMesh tests
def test_DFMesh_init():
    pass

#------------------------------------------------------------------------------
# dfb_transformation namespace
#------------------------------------------------------------------------------

def test_DFTransform_init():
    t = dfb.dfb_transformation.DFTransformation()
    assert t is not None, "DFTransformation should be initialized successfully"

def test_DFTransform_read_write(create_DFPointCloudSampleRoof):
    pc = create_DFPointCloudSampleRoof
    t = dfb.dfb_transformation.DFTransformation()

    matrix = t.transformation_matrix
    print(matrix)
    assert matrix is not None, "Transformation matrix should be initialized"

    matrix_identity = [[1.0, 0.0, 0.0, 0.0],
                       [0.0, 1.0, 0.0, 0.0],
                       [0.0, 0.0, 1.0, 0.0],
                       [0.0, 0.0, 0.0, 1.0]]

    t.transformation_matrix = matrix_identity
    assert (t.transformation_matrix == matrix_identity).all(), "Transformation matrix should be set to identity"


#------------------------------------------------------------------------------
# dfb_registrations namespace
#------------------------------------------------------------------------------
# TODO: to be implemented

#------------------------------------------------------------------------------
# dfb_segmentation namespace
#------------------------------------------------------------------------------
# TODO: to be implemented


if __name__ == "__main__":
    pytest.main()