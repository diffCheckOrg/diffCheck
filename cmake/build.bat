@echo on
REM build the project in Release mode
conda run --name diff_check --no-capture-output cmake --build build --config Release