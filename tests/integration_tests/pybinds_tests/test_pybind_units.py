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

# import data files with correct path (also for GitHub Actions)
def get_ply_cloud_roof_quarter_path():
    base_test_data_dir = os.getenv('DF_TEST_DATA_DIR', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'test_data')))
    ply_file_path = os.path.join(base_test_data_dir, "roof_quarter.ply")
    if not os.path.exists(ply_file_path):
        raise FileNotFoundError(f"PLY file not found at: {ply_file_path}")
    return ply_file_path

def get_ply_cloud_sphere_path():
    base_test_data_dir = os.getenv('DF_TEST_DATA_DIR', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'test_data')))
    ply_file_path = os.path.join(base_test_data_dir, "sphere_5kpts_with_normals.ply")
    if not os.path.exists(ply_file_path):
        raise FileNotFoundError(f"PLY file not found at: {ply_file_path}")
    return ply_file_path

def get_ply_cloud_bunny_path():
    base_test_data_dir = os.getenv('DF_TEST_DATA_DIR', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'test_data')))
    ply_file_path = os.path.join(base_test_data_dir, "stanford_bunny_50kpts_with_normals.ply")
    if not os.path.exists(ply_file_path):
        raise FileNotFoundError(f"PLY file not found at: {ply_file_path}")
    return ply_file_path

def get_ply_mesh_cube_path():
    base_test_data_dir = os.getenv('DF_TEST_DATA_DIR', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'test_data')))
    ply_file_path = os.path.join(base_test_data_dir, "cube_mesh.ply")
    if not os.path.exists(ply_file_path):
        raise FileNotFoundError(f"PLY file not found at: {ply_file_path}")
    return ply_file_path

def get_two_separate_planes_ply_path():
    base_test_data_dir = os.getenv('DF_TEST_DATA_DIR', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'test_data')))
    ply_file_path = os.path.join(base_test_data_dir, "two_separate_planes_with_normals.ply")
    if not os.path.exists(ply_file_path):
        raise FileNotFoundError(f"PLY file not found at: {ply_file_path}")
    return ply_file_path

def get_two_connected_planes_ply_path():
    base_test_data_dir = os.getenv('DF_TEST_DATA_DIR', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'test_data')))
    ply_file_path = os.path.join(base_test_data_dir, "two_connected_planes_with_normals.ply")
    if not os.path.exists(ply_file_path):
        raise FileNotFoundError(f"PLY file not found at: {ply_file_path}")
    return ply_file_path

def get_ply_plane_with_one_outlier_path():
    base_test_data_dir = os.getenv('DF_TEST_DATA_DIR', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'test_data')))
    ply_file_path = os.path.join(base_test_data_dir, "test_pc_for_SOR_101pts_with_1_outlier.ply")
    if not os.path.exists(ply_file_path):
        raise FileNotFoundError(f"PLY file not found at: {ply_file_path}")
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

def test_DFPointCloud_save_to_PLY():
    pc = dfb.dfb_geometry.DFPointCloud()
    pc.load_from_PLY(get_ply_cloud_roof_quarter_path())

    temp_ply_path = os.path.join(os.path.dirname(__file__), "temp_ply.ply")
    pc.save_to_PLY(temp_ply_path)
    assert os.path.exists(temp_ply_path), "The PLY file should be saved to the specified path"
    os.remove(temp_ply_path)

@pytest.fixture
def create_DFPointCloudSampleRoof():
    df_pcd = dfb.dfb_geometry.DFPointCloud()
    df_pcd.load_from_PLY(get_ply_cloud_roof_quarter_path())
    yield df_pcd

@pytest.fixture
def create_two_DFPointCloudSphere():
    df_pcd_1 = dfb.dfb_geometry.DFPointCloud()
    df_pcd_2 = dfb.dfb_geometry.DFPointCloud()
    df_pcd_1.load_from_PLY(get_ply_cloud_sphere_path())
    df_pcd_2.load_from_PLY(get_ply_cloud_sphere_path())
    yield df_pcd_1, df_pcd_2

@pytest.fixture
def create_two_DFPointCloudBunny():
    df_pcd_1 = dfb.dfb_geometry.DFPointCloud()
    df_pcd_2 = dfb.dfb_geometry.DFPointCloud()
    df_pcd_1.load_from_PLY(get_ply_cloud_bunny_path())
    df_pcd_2.load_from_PLY(get_ply_cloud_bunny_path())
    yield df_pcd_1, df_pcd_2

@pytest.fixture
def create_DFPointCloudTwoSeparatePlanes():
    df_pcd = dfb.dfb_geometry.DFPointCloud()
    df_pcd.load_from_PLY(get_two_separate_planes_ply_path())
    yield df_pcd

@pytest.fixture
def create_DFPointCloudTwoConnectedPlanes():
    df_pcd = dfb.dfb_geometry.DFPointCloud()
    df_pcd.load_from_PLY(get_two_connected_planes_ply_path())
    yield df_pcd

@pytest.fixture
def create_DFMeshCube():
    df_mesh = dfb.dfb_geometry.DFMesh()
    df_mesh.load_from_PLY(get_ply_mesh_cube_path())
    yield df_mesh

@pytest.fixture
def create_DFPointCloudOneOutlier():
    df_pcd = dfb.dfb_geometry.DFPointCloud()
    df_pcd.load_from_PLY(get_ply_plane_with_one_outlier_path())
    yield df_pcd

# point cloud tests

def test_DFPointCloud_properties(create_DFPointCloudSampleRoof):
    pc = create_DFPointCloudSampleRoof
    assert pc.points.__len__() == 7379, "DFPointCloud should have 7379 points"
    assert pc.normals.__len__() == 7379, "DFPointCloud should have 7379 normals"
    assert pc.colors.__len__() == 7379, "DFPointCloud should have 7379 colors"

    assert pc.get_num_points() == 7379, "get_num_points() should return 7379"
    assert pc.get_num_normals() == 7379, "get_num_normals() should return 7379"
    assert pc.get_num_colors() == 7379, "get_num_colors() should return 7379"

    assert pc.has_points(), "has_points() should return True"
    assert pc.has_colors(), "has_colors() should return True"
    assert pc.has_normals(), "has_normals() should return True"

    pc.points = []
    pc.normals = []
    pc.colors = []
    assert not pc.has_points(), "has_points() should return False"
    assert not pc.has_colors(), "has_colors() should return False"
    assert not pc.has_normals(), "has_normals() should return False"

def test_DFPointCloud_add_points():
    point_pc_1 = [(0, 0, 0)]
    point_pc_2 = [(1, 1, 1)]
    normal_pc_1 = [(0, 0, 1)]
    normal_pc_2 = [(1, 0, 0)]
    color_pc_1 = [(255, 0, 0)]
    color_pc_2 = [(0, 255, 0)]
    pc_1 = dfb.dfb_geometry.DFPointCloud(point_pc_1, normal_pc_1, color_pc_1)
    pc_2 = dfb.dfb_geometry.DFPointCloud(point_pc_2, normal_pc_2, color_pc_2)
    pc_1.add_points(pc_2)
    assert pc_1.points.__len__() == 2, "two pointclouds of 1 pt combined into one should have 2 pts"

def test_DFPointCloud_apply_color(create_DFPointCloudSampleRoof):
    pc = create_DFPointCloudSampleRoof
    pc.apply_color(255, 0, 0)
    for color in pc.colors:
        assert (color[0] == 1 and color[1] == 0 and color[2] == 0), "All colors should be (255, 0, 0)"

def test_DFPointCloud_remove_statistical_outliers(create_DFPointCloudOneOutlier):
    pc = create_DFPointCloudOneOutlier
    pc.remove_statistical_outliers(50, 4)
    assert pc.points.__len__() == 100, "DFPointCloud should have 100 points"
    assert pc.normals.__len__() == pc.points.__len__(), "DFPointCloud should have as many normals as points"
    assert pc.colors.__len__() == pc.points.__len__(), "DFPointCloud should have as many colors as points"

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
    # round to the 3 decimal places
    assert round(obb[0][0], 3) == 0.196, "The min x of the OBB should be 0.196"

def test_DFPointCloud_get_axis_aligned_bounding_box(create_DFPointCloudSampleRoof):
    pc = create_DFPointCloudSampleRoof
    aabb = pc.get_axis_aligned_bounding_box()
    # round to the 3 decimal places
    assert round(aabb[0][0], 3) == -2.339, "The min x of the AABB should be 0.196"

def test_DFPointCloud_compute_distance():
    point_pc_1 = [(0, 0, 0)]
    point_pc_2 = [(1, 0, 0)]
    normal_pc_1 = [(0, 0, 1)]
    normal_pc_2 = [(0, 0, 1)]
    color_pc_1 = [(0, 0, 0)]
    color_pc_2 = [(0, 0, 0)]

    pc_1 = dfb.dfb_geometry.DFPointCloud(point_pc_1, normal_pc_1, color_pc_1)
    pc_2 = dfb.dfb_geometry.DFPointCloud(point_pc_2, normal_pc_2, color_pc_2)

    distance = pc_1.compute_distance(pc_2)[0]

    assert distance == 1. , "The distance between the two points should be 1."

# mesh tests

def test_DFMesh_init():
    mesh = dfb.dfb_geometry.DFMesh()
    assert mesh is not None, "DFMesh should be initialized successfully"

def test_DFMesh_load_from_PLY(create_DFMeshCube):
    mesh = create_DFMeshCube
    assert mesh.vertices.__len__() == 726, "DFMesh should have 726 vertices"
    assert mesh.faces.__len__() == 1200, "DFMesh should have 800 faces"

def test_DFMesh_properties():
    vertices = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 1, -1], [0, 0, -1]]
    faces = [[0, 1, 2], [0, 2, 3], [0, 3, 4], [0, 4, 5]]
    mesh = dfb.dfb_geometry.DFMesh(vertices, faces, [], [], [])
    assert mesh.get_num_vertices() == 6, "get_num_vertices() should return 6"
    assert mesh.get_num_faces() == 4, "get_num_faces() should return 4"
    assert isinstance(mesh.vertices, list), "vertices should be a list"
    assert isinstance(mesh.faces, list), "faces should be a list"
    assert isinstance(mesh.normals_face, list), "normals_faces should be a list"
    assert isinstance(mesh.normals_vertex, list), "normals_vertex should be a list"
    assert isinstance(mesh.colors_face, list), "colors_faces should be a list"
    assert isinstance(mesh.colors_vertex, list), "colors_vertex should be a list"
    assert len(mesh.vertices[0]) == 3, "vertices should be a list of 3 coordinates"
    assert len(mesh.faces[0]) == 3, "faces should be a list of 3 indexes"

def test_DFMesh_compute_distance():
    vertices = [[0, 0, 0], [1, 0, 0], [0, 1, 0]]
    faces = [[0, 1, 2]]
    mesh = dfb.dfb_geometry.DFMesh(vertices, faces, [], [], [])
    point = [(0, 0, 1)]
    normal = [(0, 0, 1)]
    color = [(0, 0, 0)]
    pc = dfb.dfb_geometry.DFPointCloud(point, normal, color)
    distance = mesh.compute_distance(pc)[0]
    assert distance == 1.0, "The distance between the point and the mesh should be 1.0"

def test_DFMesh_sample_points(create_DFMeshCube):
    mesh = create_DFMeshCube
    pc = mesh.sample_points_uniformly(1000)
    assert pc.points.__len__() == 1000, "DFPointCloud should have 1000 points"

def test_DFMesh_compute_bounding_box(create_DFMeshCube):
    mesh = create_DFMeshCube
    obb = mesh.get_tight_bounding_box()
    assert obb[0][0] == 0, "The x coordinate of the first corner of the OBB should be 0"
    assert obb[1][0] == 100, "The y coordinate of the second corner of the OBB should be 100"
    assert obb[2][0] == 0, "The y coordinate of the third corner of the OBB should be 0"
    assert obb[6][2] == 100, "The z coordinate of the second to last corner of the OBB should be 100"

def test_DFMesh_getters(create_DFMeshCube):
    mesh = create_DFMeshCube
    assert mesh.get_num_vertices() == 726, "get_num_vertices() should return 726"
    assert mesh.get_num_faces() == 1200, "get_num_faces() should return 1200"


#------------------------------------------------------------------------------
# dfb_transformation namespace
#------------------------------------------------------------------------------

def test_DFTransform_init():
    t = dfb.dfb_transformation.DFTransformation()
    assert t is not None, "DFTransformation should be initialized successfully"

def test_DFTransform_read_write(create_DFPointCloudSampleRoof):
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
def test_DFRegistration_pure_translation(create_two_DFPointCloudSphere):

    def make_assertions(df_transformation_result):
        assert df_transformation_result is not None, "DFRegistration should return a transformation matrix"
        assert abs(df_transformation_result.transformation_matrix[0][3] - 20) < 0.5, "The translation in x should be around 20"
        assert abs(df_transformation_result.transformation_matrix[1][3] - 20) < 0.5, "The translation in y should be around 20"
        assert abs(df_transformation_result.transformation_matrix[2][3] - 20) < 0.5, "The translation in z should be around 20"

    sphere_1, sphere_2 = create_two_DFPointCloudSphere

    t = dfb.dfb_transformation.DFTransformation()
    t.transformation_matrix = [[1.0, 0.0, 0.0, 20],
                                [0.0, 1.0, 0.0, 20],
                                [0.0, 0.0, 1.0, 20],
                                [0.0, 0.0, 0.0, 1.0]]

    sphere_2.apply_transformation(t)

    df_transformation_result_o3dfgrfm = dfb.dfb_registrations.DFGlobalRegistrations.O3DFastGlobalRegistrationFeatureMatching(sphere_1, sphere_2)
    df_transformation_result_o3drfm = dfb.dfb_registrations.DFGlobalRegistrations.O3DRansacOnFeatureMatching(sphere_1, sphere_2)
    df_transformation_result_o3dicp = dfb.dfb_registrations.DFRefinedRegistration.O3DICP(sphere_1, sphere_2, max_correspondence_distance=20)
    df_transformation_result_o3dgicp = dfb.dfb_registrations.DFRefinedRegistration.O3DGeneralizedICP(sphere_1, sphere_2, max_correspondence_distance=20)

    make_assertions(df_transformation_result_o3dfgrfm)
    make_assertions(df_transformation_result_o3drfm)
    make_assertions(df_transformation_result_o3dicp)
    make_assertions(df_transformation_result_o3dgicp)


def test_DFRegistration_rotation_bunny(create_two_DFPointCloudBunny):

    def make_assertions(df_transformation_result):
        assert df_transformation_result is not None, "DFRegistration should return a transformation matrix"
        assert abs(df_transformation_result.transformation_matrix[0][0] - 0.866) < 0.2, "The rotation part of transformation matrix should be close to the transposed rotation matrix initially applied"
        assert abs(df_transformation_result.transformation_matrix[0][1]) < 0.2, "The rotation part of transformation matrix should be close to the transposed rotation matrix initially applied"
        assert abs(df_transformation_result.transformation_matrix[0][2] - 0.5) < 0.2, "The rotation part of transformation matrix should be close to the transposed rotation matrix initially applied"

    bunny_1, bunny_2 =create_two_DFPointCloudBunny

    r = dfb.dfb_transformation.DFTransformation()
    r.transformation_matrix = [[0.866, 0.0, 0.5, 0.0],
                               [0.0, 1.0, 0.0, 0.0],
                               [-0.5, 0.0, 0.866, 0.0],
                               [0.0, 0.0, 0.0, 1.0]] # 30 degree rotation around y-axis
    bunny_2.apply_transformation(r)

    df_transformation_result_o3dfgrfm = dfb.dfb_registrations.DFGlobalRegistrations.O3DFastGlobalRegistrationFeatureMatching(bunny_1, bunny_2)
    df_transformation_result_o3drfm = dfb.dfb_registrations.DFGlobalRegistrations.O3DRansacOnFeatureMatching(bunny_1, bunny_2)
    df_transformation_result_o3dicp = dfb.dfb_registrations.DFRefinedRegistration.O3DICP(bunny_1, bunny_2, max_correspondence_distance=1.0)
    df_transformation_result_o3dgicp = dfb.dfb_registrations.DFRefinedRegistration.O3DGeneralizedICP(bunny_1, bunny_2, max_correspondence_distance=15.0)

    make_assertions(df_transformation_result_o3dfgrfm)
    make_assertions(df_transformation_result_o3drfm)
    make_assertions(df_transformation_result_o3dicp)
    make_assertions(df_transformation_result_o3dgicp)


def test_DFRegistration_composite_bunny(create_two_DFPointCloudBunny):

    def make_assertions(df_transformation_result):
        assert df_transformation_result is not None, "DFRegistration should return a transformation matrix"
        assert abs(df_transformation_result.transformation_matrix[0][3] - 0.1) < 0.02, "The translation in x should be around -0.05"
        assert abs(df_transformation_result.transformation_matrix[1][3] - 0.1) < 0.02, "The translation in y should be around -0.05"
        assert abs(df_transformation_result.transformation_matrix[2][3] - 0.1) < 0.02, "The translation in z should be around 0.05"
        assert abs(df_transformation_result.transformation_matrix[0][0] - 0.866) < 0.2, "The rotation part of transformation matrix should be close to the transposed rotation matrix initially applied"
        assert abs(df_transformation_result.transformation_matrix[0][1]) < 0.2, "The rotation part of transformation matrix should be close to the transposed rotation matrix initially applied"
        assert abs(df_transformation_result.transformation_matrix[0][2] - 0.5) < 0.2, "The rotation part of transformation matrix should be close to the transposed rotation matrix initially applied"

    bunny_1 ,bunny_2 = create_two_DFPointCloudBunny

    transform = dfb.dfb_transformation.DFTransformation()
    transform.transformation_matrix = [[0.866, 0.0, 0.5, 0.1],
                                [0.0, 1.0, 0.0, 0.1],
                                [-0.5, 0.0, 0.866, 0.1],
                                [0.0, 0.0, 0.0, 1.0]] # 30 degree rotation around y-axis + translation

    bunny_2.apply_transformation(transform)

    df_transformation_result_o3dfgrfm = dfb.dfb_registrations.DFGlobalRegistrations.O3DFastGlobalRegistrationFeatureMatching(bunny_1, bunny_2)
    df_transformation_result_o3drfm = dfb.dfb_registrations.DFGlobalRegistrations.O3DRansacOnFeatureMatching(bunny_1, bunny_2)
    df_transformation_result_o3dicp = dfb.dfb_registrations.DFRefinedRegistration.O3DICP(bunny_1, bunny_2)
    df_transformation_result_o3dgicp = dfb.dfb_registrations.DFRefinedRegistration.O3DGeneralizedICP(bunny_1, bunny_2)

    make_assertions(df_transformation_result_o3dfgrfm)
    make_assertions(df_transformation_result_o3drfm)
    make_assertions(df_transformation_result_o3dicp)
    make_assertions(df_transformation_result_o3dgicp)


#------------------------------------------------------------------------------
# dfb_segmentation namespace
#------------------------------------------------------------------------------

def test_DFPlaneSegmentation_separate_plans(create_DFPointCloudTwoSeparatePlanes):
    pc = create_DFPointCloudTwoSeparatePlanes

    segments = dfb.dfb_segmentation.DFSegmentation.segment_by_normal(pc,
                                                                     normal_threshold_degree=5,
                                                                     min_cluster_size=100,
                                                                     knn_neighborhood_size=20)

    assert len(segments) == 2, "DFPlaneSegmentation should return 2 segments"

def test_DFPlaneSegmentation_connected_plans(create_DFPointCloudTwoConnectedPlanes):
    pc = create_DFPointCloudTwoConnectedPlanes

    segments = dfb.dfb_segmentation.DFSegmentation.segment_by_normal(pc,
                                                                     normal_threshold_degree=5,
                                                                     min_cluster_size=100,
                                                                     knn_neighborhood_size=20)

    assert len(segments) == 2, "DFPlaneSegmentation should return 2 segments"

if __name__ == "__main__":
    pytest.main()
