@echo off
echo ======================================================================
echo LEAGUE OF LEGENDS ANALYTICS - DEMARRAGE FRONTEND
echo ======================================================================
echo.

echo [INFO] Verifiez que l'API backend est lancee sur http://127.0.0.1:8000
echo        Si ce n'est pas le cas, lancez: python run_api.py
echo.

echo [INFO] Demarrage du serveur HTTP pour le frontend...
echo.

cd /d "%~dp0.."
cd frontend
python -m http.server 8080

echo.
echo ======================================================================
echo Frontend disponible sur : http://localhost:8080
echo Documentation API : http://127.0.0.1:8000/docs
echo ======================================================================
