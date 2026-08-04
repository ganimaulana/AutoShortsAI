@echo off
cd /d "%~dp0"

python tools\archive_chatgpt.py

echo.
echo ============================================
echo ChatGPT Archive Finished
echo ============================================

explorer .

pause