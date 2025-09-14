
@echo off
cd /d "%~dp0"
set "DC=docker compose"
%DC% version >nul 2>&1 || set "DC=docker-compose"
%DC% down
echo ✅ Stopped SignalX V11.
