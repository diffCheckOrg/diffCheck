#!/bin/zsh
########################################################################
# check if conda is available
# check that diff_check environment is available
# activate it
########################################################################

# Check if conda command is available
echo "Checking if conda command is available..."
if ! command -v conda >/dev/null 2>&1; then
    echo "conda command not found, you won't be able to build the python wrap for diffcheck. Please install Anaconda or Miniconda first."
    exit 1
fi
echo "Conda command is available."

# Check if the diff_check environment is available
if ! conda env list | grep -q 'diff_check'; then
    echo "diff_check environment not found, you should create one by running:"
    echo "$ conda env create -f environment.mac.yml"
    exit 1
else
    echo "diff_check environment is available, updating it now..."
    if conda env update --name diff_check --file environment.mac.yml --prune; then
        echo "Environment updated successfully."
    else
        echo "Failed to update diff_check environment, please check the environment.mac.yml file."
        exit 1
    fi
fi
echo "diff_check environment is up to date."

# Check if a different environment than diff_check is activated, if so deactivate it
active_env_name=$(conda info --envs | awk '/\*/ {print $1}')
if [[ "$active_env_name" != "diff_check" && -n "$active_env_name" ]]; then
    echo "You should deactivate $active_env_name first with 'conda deactivate' and 'conda activate diff_check' before running this script."
    exit 1
fi

echo "You can start the cmake config now ..."
