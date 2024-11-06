# Robotic Assembly

As a studycase for the robotic assembly, we fabricated a spatial structure with a total of thirteen elements of square section connected through bolted face lap joints. The setup included two ABB GoFa CRB 15000-5 and a human.

<br>

<p align="center">
    <img style="background-color: transparent;"
    src="./_static/tutorials/fig_additive_robotic.png" width="600">
</p>

<br>

```{eval-rst}
.. raw:: html

    <div style="display: flex; justify-content: center;">

        <a href="./_static/example_files/additive_gh_robotic_v1.gh" download style="display: inline-block; padding: 10px 20px; font-size: 16px; color: white; background-color: #28a745; text-align: center; text-decoration: none; border-radius: 5px;">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-arrow-down-circle" viewBox="0 0 16 16">
            <path fill-rule="evenodd" d="M1 8a7 7 0 1 0 14 0A7 7 0 0 0 1 8m15 0A8 8 0 1 1 0 8a8 8 0 0 1 16 0M8.5 4.5a.5.5 0 0 0-1 0v5.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293z"/>
            </svg>
            Download .gh file
        </a>

    </div>
```

## Steps

### 1. Input the data
First things first, let's import your cleaned scan and corresponding polysurface model in Rhino. For this tutorial, we assume that the two are already aligned to each other as the location of the robotically assembled structure is known.

<p align="center">
    <img style="background-color: transparent;"
    src="./_static/tutorials/fig_additive_robotic_start.png" width="600">
</p>


### 2. Build the DFAssembly
Here we convert the model of our structure into the internal datatype of diffcheck, DFAssembly.

<p align="center">
    <img style="background-color: transparent;"
    src="./_static/tutorials/fig_additive_robotic_DFassembly.png" width="500">
</p>

> DF's components:
> * [`DFAssebmly`](gh_DFBuildAssembly)

### 3.Preparation of CAD and scan data
We get the pointcloud for the CAD, reduce them to decrease the computation time and compute the normals which is necessary for the next step.

<p align="center">
    <img style="background-color: transparent;"
    src="./_static/tutorials/fig_additive_robotic_prep.png" width="1000">
</p>

```{hint}
We assume that the tranformation between the scan and the CAD model is known. If this is not the case, refer to the Registration step of the [`Manual Assembly`](manual-assembly.md#3-registration-of-cad-and-scan)
```

> DF's components:
> * [`DFBrepToCloud`](gh_DFBrepToCloud)
> * [`DFCloudVoxelDownsample`](gh_DFCloudVoxelDownsample)
> * [`DFCloudNormalEstimator`](gh_DFCloudNormalEstimator)


### 4. Segmentation of the scan
We segment the scan to isolate the parts of the raw point cloud of the scan that correspond to each beam of the assembly.

<p align="center">
    <img style="background-color: transparent;"
    src="./_static/tutorials/fig_additive_robotic_Seg.png" width="1000">
</p>

> DF's components:
> * [`DFCloudNormalSegmentator`](gh_DFCloudNormalSegmentator)
> * [`DFRemoveStatisticalOutliers`](gh_DFRemoveStatisticalOutliers)
> * [`DFJointSegmentator`](gh_DFJointSegmentator)
> * [`DFColorizeCloud`](gh_DFColorizeCloud)

### 5. Error computation
At this point we can compute the error between the CAD model and the scan. The error is computed as the distance between the closest point on the CAD model and the scan. The current DF's output metrics are:

* *distance* : the distance between the closest point on the CAD model and the scan
* *mean* : the mean distance between the closest point on the CAD model and the scan
* *max_deviation* : the maximum distance between the closest point on the CAD model and the scan
* *min_deviation* : the minimum distance between the closest point on the CAD model and the scan
* *std_deviation* : the standard deviation of the distance between the closest point on the CAD model and the scan

<p align="center">
    <img style="background-color: transparent;"
    src="./_static/tutorials/fig_additive_robotic_Error.png" width="500">
</p>

> DF's components:
> * [`DFCloudMeshDistance`](gh_DFCloudMeshDistance)

### 6. Error Visulization
DF allows you to quickly visualize the errors in the Rhino viewport. The color of the points represents the distance between the CAD model and the scan. The color scale can be adjusted to better visualize the error. We also provide a graph that shows the distribution of the errors.

<p align="center">
    <img style="background-color: transparent;"
    src="./_static/tutorials/fig_additive_robotic_Viz.png" width="600">
</p>

<div style="display: flex; justify-content: space-around; align-items: center;">
    <figure style="margin: 10px;">
        <img src="./_static/tutorials/fig_additive_robotic_results1.png" alt="subtr detail" style="height: 400px; background-color: transparent;">
        <figcaption>View of the visualization of the mean error for the analysed clouds on the CAD model itself. </figcaption>
    </figure>
    <figure style="margin: 10px;">
        <img src="./_static/tutorials/fig_additive_robotic_graph_viz.png" alt="subtr graph" style="height: 400px; background-color: transparent;">
        <figcaption>View of the graph of the corresponding distribution of the mean error directly in Rhino.</figcaption>
    </figure>
</div>

> DF's components:
> * [`DFVisualizationSettings`](gh_DFVisualizationSettings)
> * [`DFVisualization`](gh_DFVisualization)

### 7. Export the results
The results can be also exported in a CSV file for further analysis or documentation.

<p align="center">
    <img style="background-color: transparent;"
    src="./_static/tutorials/fig_additive_robotic_export.png" width="500">
</p>

The CSV contains the values per element..


| Beam ID | Min Deviation | Max Deviation | Std Deviation | RMSE  | Mean  |
|---------|---------------|---------------|---------------|-------|-------|
| 0       | 0             | 0.024         | 0.0029        | 0.0045| 0.0034|
| 1       | 0             | 0.0239        | 0.0034        | 0.0057| 0.0046|
| 2       | 0             | 0.0316        | 0.0036        | 0.0056| 0.0042|
| 3       | 0             | 0.024         | 0.0069        | 0.0088| 0.0055|
| 4       | 0             | 0.0117        | 0.0029        | 0.0053| 0.0045|
| 5       | 0             | 0.0242        | 0.0045        | 0.0067| 0.0049|
| ...     | ...           | ...           | ...           | ...   | ...   |

> DF's components:
> * [`DFCsvExporter`](gh_DFCsvExporter)