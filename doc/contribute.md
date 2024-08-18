(contrib_guide)=
# Contribute

We welcome pull requests from everyone. Please have a look at the [issue](https://github.com/diffCheckOrg/diffCheck/issues) list to see if there is something you can help with. If you have a new feature in mind, please open an issue to discuss it first.

## Code quality

We run [mypy](https://mypy.readthedocs.io/en/stable/index.html) and [] on pre-commit hooks to ensure code quality. Please make sure to run the following commands before submitting a pull request:

```console
pre-commit run --all-files
```

## How to contribute

Next, fall the following steps:

1. Fork the diffCheck repository by clicking the **Fork** button on the [diffCheck repository](https://github.com/diffCheckOrg/diffCheck). Clone the repository to your local machine:

    ```console
    git clone https://github.com/YOUR_USERNAME/diffCheck.git
    cd diffCheck
    ```

2. Next you will need to set up your development environment. You can find the instructions in the [development installation guide](dev_documentation).

3. Create a new branch for your feature:

    ```console
    git checkout -b my-feature
    ```

4. Add the diffCheck repository as a remote for convinience:

    ```console
    git remote add upstream https://github.com/diffCheckOrg/diffCheck
    ```