(contrib_guide)=
# Contribute

We welcome pull requests from everyone. Please have a look at the [issue](https://github.com/diffCheckOrg/diffCheck/issues) list to see if there is something you can help with. If you have a new feature in mind, please open an issue to discuss it first.

## Code quality

We run [mypy](https://mypy.readthedocs.io/en/stable/index.html) and [Ruff](https://docs.astral.sh/ruff/) for e.g. python on pre-commit hooks to ensure code quality. 
Please make sure to:
1. (when you `git clone` the repo) to install the *pre-commit hooks*:
   
   ```console
    pre-commit install
    ```
2.  to run the following commands before submitting a pull request:
    
    ```console
    pre-commit run --all-files
    ```

## How to contribute

Follow these steps to contribute to the project:

1. Fork the diffCheck repository by clicking the **Fork** button on the [diffCheck repository](https://github.com/diffCheckOrg/diffCheck). Clone the repository to your local machine:

    ```console
    git clone --recurse-submodules https://github.com/YOUR_USERNAME/diffCheck.git
    cd diffCheck
    ```

2. Create a new branch for your feature:

    ```console
    git checkout -b my-feature
    ```

3. Add the diffCheck repository as a remote for convinience:

    ```console
    git remote add upstream https://github.com/diffCheckOrg/diffCheck
    ```

4. Next you will need to set up your development environment. You can find the instructions in the [development installation guide](dev_env).

5. Work on your feature (follow [c++](cpp_conv) or [py](py_conv) style guide) and commit your changes by following the [commit message guidelines](git_commit_system):

    ```console
    git add .
    git commit -m "WIP: Add my feature"
    git push origin my-feature
    ```
