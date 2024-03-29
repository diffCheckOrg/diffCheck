# Use the latest Windows Server Core image with .NET Framework 4.8.
FROM mcr.microsoft.com/windows/servercore:ltsc2019

# Restore the default Windows shell for correct batch processing.
SHELL ["cmd", "/S", "/C"]

# Download and install CMake
ADD https://github.com/Kitware/CMake/releases/download/v3.21.1/cmake-3.21.1-win64-x64.msi C:\\temp\\cmake.msi
RUN powershell Start-Process -FilePath msiexec.exe -ArgumentList '/i', 'C:\\temp\\cmake.msi', '/quiet', '/norestart' -NoNewWindow -Wait

# Download and install Git
ADD https://github.com/git-for-windows/git/releases/download/v2.33.0.windows.2/Git-2.33.0.2-64-bit.exe C:\\temp\\git.exe
RUN powershell Start-Process -FilePath C:\\temp\\git.exe -ArgumentList '/VERYSILENT' -NoNewWindow -Wait

# Set up the working directory
WORKDIR C:/project

# make the code available in the container
COPY . .

# Run the cmake/config.bat script
RUN ["cmd", "/S", "/C", "cmake -DCMAKE_TOOLCHAIN_FILE=C:\\vcpkg\\scripts\\buildsystems\\vcpkg.cmake -S . -B build -G "Visual Studio 16 2019" -A x64"]

# Run the build script
RUN ["cmd", "/S", "/C", "cmake --build build --config Release"]
