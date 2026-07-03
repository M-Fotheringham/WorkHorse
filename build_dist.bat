@echo off
setlocal

REM Build WorkHorse as a standalone Windows app using Nuitka.
REM Run this from the repo root:
REM     build_dist.bat

set APP_NAME=WorkHorse
set ENTRY_POINT=src\workhorse\main.py
set ICON_FILE=docs\_figs\workhorse_logo.ico
set OUTPUT_DIR=build

python -m pip install --upgrade nuitka ordered-set zstandard

python -m nuitka ^
  --standalone ^
  --windows-console-mode=disable ^
  --enable-plugin=pyside6 ^
  --windows-icon-from-ico=%ICON_FILE% ^
  --include-package=workhorse ^
  --include-data-dir=docs=docs ^
  --output-dir=%OUTPUT_DIR% ^
  --output-filename=%APP_NAME%.exe ^
  %ENTRY_POINT%

echo.
echo Build complete.
echo Your distributable app folder should be in:
echo %OUTPUT_DIR%\main.dist
echo.
echo Run:
echo %OUTPUT_DIR%\main.dist\%APP_NAME%.exe

endlocal