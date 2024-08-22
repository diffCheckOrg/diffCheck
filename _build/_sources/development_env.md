(dev_env)=
# Development environment

If you develop for DF, you need to set up your development environment. This guide will help you to do that. Wether you are developing for the `c++` or `python` part of the project, you will find the necessary information here.

## Prepare your environment

Before to start, especially if you used diffCheck as an end-user before you will need to:

1. Make sure to have `camke` installed on your machine. You can download it [here](https://cmake.org/download/).
2. Make sure to have `git` installed on your machine. You can download it [here](https://git-scm.com/downloads).
3. We recommend to use `Visual Studio Code` as an IDE. You can download it [here](https://code.visualstudio.com/) together with [script-sync](https://github.com/ibois-epfl/script-sync) extension for Rhino/Grasshopper. You can download it from the Rhino's `PackageManager`. It is particularly useful if you want to develop [GHComponents](gh_components_gd) in python.
4. if you used diffCheck before as an end-user clean all the `diffCheck folders` in the following directory (the last name will change), beware that Rhino should be closed before this step:
    ```console
    C:\Users\<user-name>\.rhinocode\py39-rh8\site-envs\default-wMh5LZL3
    ```

    ```{important}
    if you drop an official released diffCheck component from yak, this one will have the `#r : diffCheck==<version_number>` notation at the top of the script. Get rid of all these release components before to start and be sur to erase again the previous folders (they recreated each time `#r : diffCheck` is called).
    ```

5. Clone the repository on your machine. Open a terminal and run the following command:
    ```console
    git clone https://github.com/diffCheckOrg/diffCheck
    ```

6. Checkout the repo:
    ```console
    cd diffCheck
    ```

7. Run cmake utilities `.bat`s files to config and build:
    ```console
    ./cmake/config.bat
    ./cmake/build.bat
    ```

8. Build the python df package from the py source code's directory:
   ```console
   cd src/gh/diffCheck
   python setup.py sdist bdist_wheel
   ```

9. Last, install the pip pacakge from the repository in editable mode. This way, all the modifications made to the source code of the repository will be reflected in the installed package. Open a terminal and run the following command (replace the path with where you download the repository):
    ```console
    C:\Users\<your-username>\.rhinocode\py39-rh8\python.exe -m pip install -e "<path-to-repository-root>\src\gh\diffCheck"
    ```

    ```{note}
    For your info the packages is installed in `C:\Users\andre\.rhinocode\py39-rh8\Lib\site-packages`.
    ```

That's it you are now a contributor to the diffCheck! We raccomand to not download anymore from yak package but rather use the source code in the repository. If you want the latest diffCheck, checkout and pull the main.

---

(c-df-build)=
## C++ DF build
We mainly code in C++ to have heavy-lifting operations accessible via a [pybind11 interface](../src/diffCheckBindings.cc). If you or someone else has modified one of two follow these steps:

1. Checkout the repository:
    ```console
    cd diffCheck
    ```
2. Run cmake utilities `.bat`s files to config and build:
    ```console
    ./cmake/config.bat
    ./cmake/build.bat
    ```
3. All the C++'s targets should be now built.

---

## Python DF build
There are 3 ways to develop in python in DF, often you will do both at the same time:
* Develop `GHComponents` in python
* Develop the `pybind11` interface in c++
* Develop the Python's `diffCheck` API

(gh_components_gd)=
### a) Develop `GHComponents` in API
We follow the Compas's method to generate [DF python components](gh_dfcomp) in Grasshopper, have a look at their [guide](https://github.com/compas-dev/compas-actions.ghpython_components). All the components are in `src/gh/components`. To develop a new component, you will need to follow these steps:

1. Create a new folder in `src/gh/components` with the name of your component.
2. Create 3 files with the following names in it:
    * a) `code.py`: this is where you code goes
    * b) `icon.png`: this is the icon of your component
    * c) `metadata.json`: this is the metadata of your component (for more info follow [Compas guidelines](https://github.com/compas-dev/compas-actions.ghpython_components?tab=readme-ov-file#metadata))
  
    your `code.py` should look like this:

    ```{eval-rst}
    .. literalinclude:: ../src/gh/components/DF_tester/code.py
        :language: python
        :linenos:
        :caption: `DF_tester component <../src/gh/components/DF_tester/code.py>`_
    ```
3. To test it in Grasshopper, drop a new `script-sync` component in Grasshopper, point it to the `code.py` file and add `diffCheck` to the packages to reload of the component.
4. Finally, you will need to add the following on your last line of the `code.py` file:
    ```python
    if __name__ == "__main__":
        comp = DF_tester()
        o_value : bool = comp.Run()
    ```

    ```{warning}
    This is necessary to run the component in the Rhino's python editor but it should be **removed** when done.
    ```
5. Once you are satisfied you can componentize it by running:
    ```console
    invoke ghcomponentize
    ```
    This will generate the component in the `build/gh` folder. Grab yours and drop it on the Grasshopper canvas, be sure that this is working as expected.

    ```{hint}
    If you pull a new version of the source code with new components you will need to run this command to update the generate the components, erase the old ones in the `ghuser` folder and add the new ones.
    ```
6. Done! You have now a new component in the `ghuser` tab of Grasshopper.

(pybind_gd)=
### b) Develop the `pybind11` interface in c++

Have a look at [C++ DF build](#c-df-build) to build the c++ project. The `pybind11` interface is in the `src/diffCheckBindings.cc` file. Write your new functions or namespace in this file. This is basically a `.dll` so for Rhino/Grasshopper to be visible you need to first close Rhino and run `cmake/build.bat` to build the project. Once done, you can open Rhino and test your new wrap functions in the Rhino's python editor.


(dfpypack_gd)=
### c) Develop the Python's `diffCheck` API

All the source code is in the `src/gh/diffCheck/diffCheck` folder. If you add new modules or code to existing one and you are using `script-sync` to test your code in Grasshopper, your changes will be immediately reflected. Have a look at the [diffCheck Python API](diffCheck_API) for more info.

```{note}
If you want to test your code in the Rhino's python editor, you will need to install the package in editable mode. Have a look at the [Prepare your environment](#prepare-your-environment) section for more info.
```