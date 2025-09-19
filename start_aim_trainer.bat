@echo off
setlocal enabledelayedexpansion

set "PROJECT_ROOT=%~dp0"
if "%PROJECT_ROOT:~-1%"=="\" set "PROJECT_ROOT=%PROJECT_ROOT:~0,-1%"

set "VENV_DIR=%PROJECT_ROOT%\.venv"
if not exist "%VENV_DIR%" (
    echo Creating virtual environment in %VENV_DIR%...
    py -3.11 -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo Failed to create virtual environment. Ensure Python 3.11 is installed.
        exit /b 1
    )
)

call "%VENV_DIR%\Scripts\activate.bat"
if errorlevel 1 (
    echo Failed to activate virtual environment.
    exit /b 1
)

echo Upgrading pip...
python -m pip install --upgrade pip >nul

if exist "%PROJECT_ROOT%\requirements.txt" (
    echo Installing project dependencies...
    python -m pip install -r "%PROJECT_ROOT%\requirements.txt"
) else (
    echo No requirements.txt found. Skipping dependency install.
)

echo Applying database migrations...
python "%PROJECT_ROOT%\manage.py" migrate
if errorlevel 1 goto :error

echo Generating target assets...
python "%PROJECT_ROOT%\manage.py" generate_target_assets
if errorlevel 1 goto :error

echo Starting Django development server...
python "%PROJECT_ROOT%\manage.py" runserver
goto :eof

:error
echo Script failed. See messages above for details.
exit /b 1
