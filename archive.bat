@echo off
setlocal

echo =====================================
echo AutoShortsAI Archive
echo =====================================

cd /d "%~dp0"

if exist AutoShortsAI_Source.zip del AutoShortsAI_Source.zip

git archive --format=zip --output=AutoShortsAI_Source.zip HEAD

if exist AutoShortsAI_Source.zip (
    echo.
    echo SUCCESS!
    echo AutoShortsAI_Source.zip created.
    explorer .
) else (
    echo.
    echo FAILED!
    echo Make sure all files are committed to Git.
)

pause