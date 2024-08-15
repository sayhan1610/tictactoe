@echo off
set /p commitMessage=Enter commit message: 
git add .
git commit -m "%commitMessage%"
git push origin main
echo Commit Complete...
echo Opening commits page...
start https://github.com/sayhan1610/artworks/commits/main/
Echo Exiting script...
timeout 5 >nul
exit