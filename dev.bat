@echo off
echo FitTrackAI - Development Commands
echo ==================================

if "%1"=="install" (
    echo Installing dependencies...
    pip install -r requirements.txt
) else if "%1"=="run" (
    echo Starting FitTrackAI...
    python app.py
) else if "%1"=="test" (
    echo Running tests...
    python -m pytest tests/ -v
) else if "%1"=="format" (
    echo Formatting code...
    black app.py tests/
) else if "%1"=="lint" (
    echo Running linting...
    flake8 app.py tests/
) else if "%1"=="help" (
    echo Available commands:
    echo   install  - Install dependencies
    echo   run      - Run the application
    echo   test     - Run tests
    echo   format   - Format code with black
    echo   lint     - Run linting with flake8
    echo   help     - Show this help
) else (
    echo Usage: dev.bat [command]
    echo Commands: install, run, test, format, lint, help
    echo.
    echo Example: dev.bat run
) 