@echo off
echo ============================================
echo    TRINITY CLI INSTALLER
echo    Three minds, one convergence
echo ============================================
echo.

echo Step 1: Installing dependencies...
pip install requests click rich

echo.
echo Step 2: Installing Trinity CLI...
pip install -e C:\Users\dwrek\trinity-cli

echo.
echo Step 3: Testing installation...
python -m trinity_cli.cli --version

echo.
echo ============================================
echo    INSTALLATION COMPLETE!
echo ============================================
echo.
echo USAGE (run these commands):
echo.
echo   python -m trinity_cli.cli ask How do I fix a CORS error
echo   python -m trinity_cli.cli review myfile.py
echo   python -m trinity_cli.cli debug TypeError undefined
echo   python -m trinity_cli.cli code Create a login function
echo.
echo SHORTCUT: Create an alias by running:
echo   doskey trinity=python -m trinity_cli.cli $*
echo.
echo Then you can use: trinity ask How do I...
echo.
echo For help: python -m trinity_cli.cli --help
echo.
pause
