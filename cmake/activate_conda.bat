@echo off
setlocal

:: ########################################################################
:: check if conda is available > 
:: check that diff_check environment is available > 
:: activate it
:: ########################################################################

:: Check if conda command is available
echo Checking if conda command is available...
where conda >nul 2>nul
if %ERRORLEVEL% equ 0 (
    echo Conda command is available.
    goto :end
)
if exist "%USERPROFILE%\Anaconda3" (
    echo Anaconda3 found in %USERPROFILE%\Anaconda3.
    goto :end
)
if exist "%ProgramData%\Anaconda3" (
    echo Anaconda3 found in %ProgramData%\Anaconda3.
    goto :end
)
if exist "%ProgramFiles%\Anaconda3" (
    echo Anaconda3 found in %ProgramFiles%\Anaconda3.
    goto :end
)
echo Anaconda3 not found, you won't be able to build the python wrap for diffcheck. Please install it first.
exit /b 1

:end
echo Anaconda3 found.

:: Check if the diff_check environment is available
call conda env list | findstr /C:"diff_check" >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo diff_check environment not found, you should create one by running:
    echo $ conda env create -f environment.yml
    exit /b 1
) else (
    echo diff_check environment is available, updating it now...
    conda env update --name diff_check --file environment.yml --prune && (
        echo Environment created successfully.
    ) || (
        echo Failed to update diff_check environment, please check the environment.yml file.
        exit /b 1
    )
)
echo diff_check environment is up to date.

:: check if a different environment then diff_check is activated, if so deactivate it
for /f "delims=" %%i in ('conda env list ^| findstr /C:"*"') do set "active_env=%%i"
for /f "delims= " %%j in ("%active_env%") do set "active_env_name=%%j"
if not "%active_env_name%"=="diff_check" (
    echo You should deactivating %active_env_name% first with "conda deactivate" and "conda activate diff_check" before running this script.
    exit /b 1
)

echo you can start the cmake config now ...