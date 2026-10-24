@echo off
cd /d "%~dp0.."
python main.py --vfs vfs\deep.csv --script startup\nope.txt
python main.py --script
python main.py --foo
