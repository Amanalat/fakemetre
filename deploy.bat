@echo off
cd /d "%~dp0"
git add index.html questions_fr.js questions_en.js
git add images/
git add NOUVEAUTES.md PROMPTS_IMAGES.md TODO_FAKEMETRE.md
git add deploy.bat watch_and_deploy.ps1
git commit -m "Mise a jour %date%"
git push
pause
