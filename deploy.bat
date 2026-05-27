@echo off
cd /d "%~dp0"
git add -A
git commit -m "Images: compression PNG->JPEG (-94%%), integration img refs dans questions_fr/en.js"
git push
pause
