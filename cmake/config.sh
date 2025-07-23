# activate the conda diff_check environment otherwise the python wrap won't work
call cmake/activate_conda.sh

#configure the project
conda run --name diff_check --no-capture-output cmake -S . -B build -DCMAKE_BUILD_TYPE=Release