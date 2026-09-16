@echo off
setlocal
title Northern France CO2 Model - PR Transport + Environmental Study
cd /d "%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0launch_dashboard.ps1"
if errorlevel 1 (
  echo.
  echo The model could not start. Please keep this window open and share the message above.
  pause
)
endlocal
