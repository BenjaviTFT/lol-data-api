@echo off
echo ======================================================================
echo LEAGUE OF LEGENDS ANALYTICS - DEMARRAGE
echo ======================================================================
echo.

echo [1] Verification de l'environnement...
python --version
echo.

echo [2] Verification de la base de donnees...
python -c "import sys; sys.path.insert(0, '.'); from db.connection import get_connection; conn = get_connection(); print('PostgreSQL: OK'); conn.close()"
echo.

echo [3] Lancement de l'API...
echo.
echo API disponible sur : http://127.0.0.1:8000
echo Documentation Swagger : http://127.0.0.1:8000/docs
echo.
echo Appuyez sur CTRL+C pour arreter l'API
echo.
python run_api.py
