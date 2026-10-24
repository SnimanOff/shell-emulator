@echo off
cd /d "%~dp0.."
python main.py --vfs vfs\minimal.csv --script startup\stage3.txt
python main.py --vfs vfs\files.csv --script startup\stage3.txt
python main.py --vfs vfs\deep.csv --script startup\stage3.txt
