@echo off
setlocal

:: run the following in a pop up window to avoid the console window and ask to ru n ass admin
@echo off
:: BatchGotAdmin
:-------------------------------------
REM  --> Check for permissions
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"

REM --> If error flag set, we do not have admin.
if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"

    "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    if exist "%temp%\getadmin.vbs" ( del "%temp%\getadmin.vbs" )
    pushd "%CD%"
    CD /D "%~dp0"
:--------------------------------------



:: Define the download URL and the target directory
set "url=https://github.com/isl-org/Open3D/releases/download/v0.18.0/open3d-devel-windows-amd64-0.18.0.zip"
set "targetDir=C:\Program Files\Open3Dtest"

:: Create the if the directory does not exist
if not exist "%targetDir%" mkdir "%targetDir%

:: check if the directory was created
if not exist "%targetDir%" (
    echo Failed to create the target directory.
    exit /b 1
)

:: Download the file
echo Downloading Open3D...
curl -L -o "%filePath%" "%url%"

:: check if the file was downloaded if not wait
:wait
if not exist "%filePath%" (
    echo Waiting for download to complete...
    timeout /t 5 /nobreak >nul
    goto wait
)
echo File downloaded.

:: Extract the file
echo Extracting Open3D...
powershell -Command "Expand-Archive -Path '%targetDir%\open3d.zip' -DestinationPath '%targetDir%'"

:: Delete the downloaded zip file
del "%targetDir%\open3d.zip"

:: Change to the target directory
cd /d "%targetDir%"

:: Run the cmake commands
echo Building Open3D...
cmake -DBUILD_WEBRTC=OFF -DBUILD_SHARED_LIBS=ON -G "Visual Studio 16 2019" -A x64 -DCMAKE_INSTALL_PREFIX="%targetDir%" -S . -B build
if errorlevel 1 (
    echo Failed to run cmake configuration command.
    exit /b 1
)

cmake --build build --config Release --target ALL_BUILD
if errorlevel 1 (
    echo Failed to build ALL_BUILD.
    exit /b 1
)

cmake --build build --config Release --target INSTALL
if errorlevel 1 (
    echo Failed to install.
    exit /b 1
)

echo Done.
endlocal