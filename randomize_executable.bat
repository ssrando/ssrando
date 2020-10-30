rm -f SOUE01.wbfs SOUE01.wbf1
"%~dp0ssrando.exe"
if %errorlevel% neq 0 exit /b %errorlevel%
wit -P copy -z modified-extract SOUE01.wbfs
pause