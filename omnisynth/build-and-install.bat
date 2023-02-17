@ECHO OFF

echo "Building wheel..."
python -m build
echo "Installing wheel..."
cd dist/
for /f %%i in ('dir /b/a-d/od/t:c') do set WHEEL_FILE=%%i
pip install --force-reinstall %WHEEL_FILE%