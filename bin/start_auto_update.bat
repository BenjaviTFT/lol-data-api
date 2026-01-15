@echo off
echo ======================================================================
echo SERVICE D'AUTO-UPDATE - TOUTES LES 10 MINUTES
echo ======================================================================
echo.
echo Ce script va mettre a jour automatiquement les donnees toutes les 10 min
echo.
echo IMPORTANT: Laisse cette fenetre ouverte en arriere-plan
echo Appuie sur Ctrl+C pour arreter le service
echo.
echo ======================================================================
echo.
pause
echo.

cd /d "%~dp0.."
python scripts\auto_update_service.py
