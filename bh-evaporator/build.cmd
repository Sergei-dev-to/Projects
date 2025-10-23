@echo off
REM Wrapper to bypass PowerShell execution policy and build the PDF
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0build.ps1" %*
exit /b %ERRORLEVEL%

