# tasks.py
from invoke import task

PATH_MANIFEST = "./manifest.yml"
PATH_SETUP = "./src/gh/diffCheck/setup.py"
PATH_INIT = "./src/gh/diffCheck/diffCheck/__init__.py"
PATH_CMAKE = "./CMakeLists.txt"
DIR_IN_GHUSER_COMPONENTS = "./src/gh/components"
DIR_OUT_GHUER_COMPONENTS = "./build/gh"


@task
def versionize(c):
    path_versionize = "./invokes/versionize.py"
    c.run(f"python {path_versionize} \
        --from-manifest \
        --path-manifest {PATH_MANIFEST} \
        --path-setup {PATH_SETUP} \
        --path-init {PATH_INIT} \
        --path-cmake {PATH_CMAKE} \
    ")

@task
def ghcomponentize(c):
    path_ghcomponentizer = "./invokes/ghcomponentize/ghcomponentizer.py"
    c.run(f"python {path_ghcomponentizer} \
        --ghio ./invokes/ghcomponentize/ghio \
        {DIR_IN_GHUSER_COMPONENTS} \
        {DIR_OUT_GHUER_COMPONENTS}")


@task
def flagerize(c, package_name="ACPy"):
    path_flagerize = "./invokes/flagerize.py"
    c.run(f"python {path_flagerize} --package {package_name} --from-manifest")

@task
def pypireize(c):
    path_pypireize = "./invokes/pypireize.py"
    c.run(f"python {path_pypireize} --setup-path ./py/pypi/setup.py")

@task
def yakerize(c):
    path_yakerize = "./invokes/yakerize/yakerize.py"
    gh_components_dir = "./build/gh"
    build_yak_dir = "./build/yak"
    c.run(f"python {path_yakerize} --gh-components-dir {gh_components_dir} --build-dir {build_yak_dir}")