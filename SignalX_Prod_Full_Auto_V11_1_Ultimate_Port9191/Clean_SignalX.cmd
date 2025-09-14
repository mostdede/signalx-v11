
@echo off
cd /d "%~dp0"
echo This will stop containers and remove images for SignalX V11 only.
set "DC=docker compose"
%DC% version >nul 2>&1 || set "DC=docker-compose"
%DC% down --rmi local -v
docker image prune -f >nul
echo ✅ Cleaned local resources for SignalX V11.
pause
