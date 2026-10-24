@echo off
cd /d "%~dp0.."
echo exit | python main.py
echo.
python main.py --script startup\stage2.txt
python main.py --vfs vfs\deep.csv --script startup\stage2.txt
