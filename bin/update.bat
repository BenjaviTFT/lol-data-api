@echo off
echo ======================================================================
echo MISE A JOUR DES DONNEES LOL
echo ======================================================================
echo.

cd /d "%~dp0.."
python scripts\update_matches.py

echo.
echo ======================================================================
echo MISE A JOUR TERMINEE
echo ======================================================================
echo.
echo Le site web affichera les nouvelles donnees apres rafraichissement
echo (Ctrl+Shift+R dans le navigateur)
echo.
pause
