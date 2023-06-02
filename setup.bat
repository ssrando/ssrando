py -m pip install poetry
poetry install
wit extract disc.iso actual-extract
mkdir modified-extract
xcopy /E /I actual-extract modified-extract
pause