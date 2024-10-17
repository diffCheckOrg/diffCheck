(doc_guide)=
# Documentation

In DF we use `Sphinx` to generate the documentation. The documentation is written in `reStructuredText` and `Markdown` and the source files are located in the `doc` folder. The documentation is hosted on `ReadTheDocs` and is automatically updated when a new commit is pushed to the `main` branch.

```{note}	
  For more info on how to write `.rst` files, check this [reStructuredText](https://canonical-documentation-with-sphinx-and-readthedocscom.readthedocs-hosted.com/style-guide/) guide.
```	

## Build locally

To build locally the documentation to test your changes:
```console
invoke documentize
```
and to open the documentation in your browser:
```console
start _build/index.html
```
If you modify the `doc`s files and refresh the pages updates will be visible.

## Contribute to the documentation

Follow these guides to contribute to the documentation whether you:

- add a new [GHComponents](ghcomp_doc_g)
- add/modify the [Python API](pyapi_doc_g)
- add a new [tutorial](tutorial_doc_g)

---
(ghcomp_doc_g)=
### ✔️ `GHComponent`'s docs

If you write a new [GHComponents](gh_components.rst) you will most probably already have created and filled a `metadata.json` file. DF uses this file to automatically generate the documentation for the GHComponents. The only thing you need to do is:
* add a new `.rst` file with the name of the component like `gh_DFComponentName.rst`
* add it to the `gh_components.rst` file's `list-table::`
  ```{attention}
    The `list-table::` is organized in two columns so if not pair add simply two empty strings `-` to the end of the last entry.
* add it to the `toctree::`

Our custom sphinx extension `sphinx_ghcomponent_parser` will automatically parse the `metadata.json` file and generate the documentation for the GHComponent✨✨.


(pyapi_doc_g)=
### ☑️ `Python API`'s docs

For [Python API documentation](diffCheck_PythonAPI), we use `sphinx-apidoc` to automatically generate the API documentation so the only thing to do is to add beautiful docstrings to the Python code with the following reStructuredText (reST) format style:

```python
    def example_function(param1, param2):
    """
    Summary of the function.

    :param param1: Description of `param1`.
    :type param1: int
    :param param2: Description of `param2`.
    :type param2: str
    :return: Description of the return value.
    :rtype: bool
    """
    return True
```

(tutorial_doc_g)=
### ✅ `DF Tutorial`'s docs

If you need to add a new page to the [tutorials](tutorials.rst) (e.g. a [new tutorial](tutorials.rst)), you can do so by adding a new `.rst` file in the `doc` folder and linking it in the `tutorials.rst` file's toctree:

```{eval-rst}
.. literalinclude:: tutorials.rst
   :language: rst
   :lines: 6-14