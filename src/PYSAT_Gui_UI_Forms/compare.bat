md .\Finished\
for /r %%i in (".\PythonUI\*.py") do findstr /v /g:".\PythonUI\10_mainwindow_empty_UI.py" "%%i" > ".\Finished\%%~ni.py"