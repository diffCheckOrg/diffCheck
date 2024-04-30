# tasks.py
from invoke import task

@task
def ghcomponentize(c):
    path_ghcomponentizer = "./invokes/ghcomponentize/ghcomponentizer.py"
    c.run(f"python {path_ghcomponentizer} --ghio ./invokes/ghcomponentize/ghio ./py/components ./build/gh")

@task
def versionize(c):
    path_versionize = "./invokes/versionize.py"
    c.run(f"python {path_versionize} --from-manifest")

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