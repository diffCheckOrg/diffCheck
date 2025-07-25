# Deploy on Mac dev log
## Current status
- The pybind part can be successfully compiled and run on mac, within Grasshopper
- Some functions do not work; Grasshopper would crash without any information once the function is called (which is also very hard to debug). Based on the current experiment, these functions are problematic:
    - `dfb_segmentation.DFSegmentation.associate_clusters`

## Run
To just run on Mac (using the pre-compiled stuff), please navigate to the folder `/portability_experiment`.
If you want to compile, follow the instruction below:

1. Make sure that `/deps/open3d/mac/open3d-devel-darwin-arm64-0.18.0/lib/cmake/Open3D` exist.
2. Run the cmake & build as usual (make sure that you're using python3.9!)
```
mkdir build_mac
cd build_mac
cmake .. -DRUN_TESTS=OFF
make -j
```
3. After building, you should see this file `/src/gh/diffCheck/diffCheck/diffcheck_bindings.cpython-39-darwin.so`
4. Go to `src/gh/diffCheck` and build the wheel, and you should see the `diffcheck-1.3.0-py3-none-any.whl` appear in a sub-folder `dist`.
```
cd ..
cd src/gh/diffCheck
python setup.py bdist_wheel
```
4. Install diffCheck to Grasshopper's python
```
/Users/petingo/.rhinocode/py39-rh8/python3.9 -m pip install dist/diffcheck-1.3.0-py3-none-any.whl --force-reinstall
```
5. You should be able to use diffCheck in Grasshopper's python now.

## Changes to mac build
- Everything in `diffcheck_binding` is now a part of `diffCheck` Instead of doing
```
from diffcheck_binding import xxx
```
You need to change it to
```
from diffCheck import xxx
```