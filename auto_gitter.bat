@echo off
:top
for /f "delims=" %%I in ('dir %USERPROFILE% /b/o/w/s ^| find /i "cmd\git.exe"') do (
	%%I config remote.origin.url git@github.com:tisaconundrum2/PySAT.git
	%%I pull origin dev
	%%I add -A
	%%I commit -m "Auto Generated Update"
	%%I push -u origin dev
	timeout /t 600
)
goto :top