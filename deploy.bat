@echo off
cd /d "%~dp0"
git add -A
git commit -m "Mise a jour %date%"
git push
pause
