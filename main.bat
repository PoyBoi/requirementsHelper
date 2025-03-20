@echo off
setlocal

:: Check if current folder is named "requirementsHelper"
for %%a in ("%CD%") do set "CurrDir=%%~nxa"
if /I "%CurrDir%"=="requirementsHelper" (
    echo Current folder is "requirementsHelper". Updating repository...
    git pull
    echo Running requirementsHelper...
    python main.py
    goto end
)

set "REPO=https://github.com/PoyBoi/requirementsHelper.git"
set "DIR=requirementsHelper"

if not exist "%DIR%" (
    echo Cloning repository...
    git clone %REPO%
) else (
    echo Repository exists. Updating...
    pushd "%DIR%"
    git pull
    popd
)

echo Running requirementsHelper...
pushd "%DIR%"
python main.py
popd

:end
pause
