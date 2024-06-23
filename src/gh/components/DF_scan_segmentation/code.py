import Rhino
import diffCheck.df_cvt_bindings as df_cvt
import diffCheck.df_geometries as df_geo
import diffCheck.diffcheck_bindings as df_bindings

def main(model, voxel_size, normal_threshold, min_cluster_size, knn_neighborhood_size):
    a = []
    df_scan = df_cvt.cvt_rhcloud_2_dfcloud(scan)
    res = df_bindings.dfb_segmentation.DFSegmentation.segmentation_point_cloud(df_scan, voxel_size, normal_threshold, min_cluster_size, false, 10, knn_neighborhood_size)
    print(len(res))
    for pc in res:
        a.append(pc)
    return a

if __name__ == "__main__":
    a = main(model, voxel_size, normal_threshold, min_cluster_size, knn_neighborhood_size)
    
