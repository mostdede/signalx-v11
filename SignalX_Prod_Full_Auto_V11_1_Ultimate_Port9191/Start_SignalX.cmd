
@echo off
setlocal ENABLEDELAYEDEXPANSION
cd /d "%~dp0"
set "DC=docker compose"
%DC% version >nul 2>&1 || set "DC=docker-compose"
echo Building SignalX V11 (backend + prebuilt frontend)...
%DC% build || (echo [ERROR] Build failed.& pause & exit /b 1)
echo Starting services...
%DC% up -d || (echo [ERROR] Up failed.& pause & exit /b 1)
echo Waiting for backend health...
for /l %%i in (1,1,30) do (
  docker inspect -f "{{json .State.Health.Status}}" signalx_backend_v11 2>nul | findstr /i "healthy" >nul && goto :ok
  timeout /t 2 >nul
)
echo [WARN] Backend not healthy yet.
:ok
echo.
echo ✅ SignalX V11 is up at http://localhost:9191/
echo API health:  http://localhost:9191/api/health
start "" http://localhost:9191/
endlocal
