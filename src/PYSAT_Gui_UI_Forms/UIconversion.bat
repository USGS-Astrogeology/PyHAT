md .\PythonUI
echo off && cls
for /r %%i in ("\UI Files\*.ui") do pyuic "%%i" > .\PythonUI\%%~ni.py