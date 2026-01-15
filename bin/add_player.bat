@echo off
echo ======================================================================
echo AJOUT D'UN NOUVEAU JOUEUR
echo ======================================================================
echo.

cd /d "%~dp0.."
python scripts\add_player.py

pause
