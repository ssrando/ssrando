py -m pip install -r requirements.txt
wit extract disc.iso actual-extract
mkdir modified-extract
xcopy /E /I actual-extract modified-extract
pause