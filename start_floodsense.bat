@echo off
title FloodSense AI - Command Center
echo ===========================================================================
echo       FLOODSENSE AI - FLOOD EARLY WARNING SYSTEM
echo ===========================================================================
echo Starting FastAPI Backend + Microsoft SQL Server Telemetry Service...
echo.

start http://localhost:8000
py backend/run_server.py
pause
