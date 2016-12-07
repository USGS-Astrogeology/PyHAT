- "UI Files" holds many *.UI
- process all these UI files with "UIconversion.bat"
- UI conversion converts all the *.ui files to *.py and puts them into "PythonUI"
- compare takes all the *.py files, and compares it against "10_mainwindow_empty_UI.py"
- take the differences and place them into FINISHED

All the files in FINISHED can then be copied and placed into their respective UI modules


Example of how this works, and how this looks
* if you are viewing this in Notepad
* make sure to have Word Wrap turned off
* this way formatting of the below example 
* is not lost 
**Note that example.py is the python version of whatever was in ui. (IT IS NOT directly copying the insides of .ui file.)

      ~/UI files/example.ui                     ~/PythonUI/example.py                    ~/PythonUI/mainwindow_empty.py
       |------------------|                      |------------------|                     |------------------|
       | <some content>   |                      |  some content    |                     |  some content    |
       | <more xml cont>  |                      |  more xml cont   |                     |  more xml cont   |
       | <this is wrong>  |      convert         |  this is wrong   |  compare these      |                  |
       | <formatting>     |     using            |  formatting      |  two files using    |                  |
       | <technically>    |    UIconversion.bat  |  technically     |  compare.bat        |                  |
       | <speaking>       | -------------------> |  speaking>       | ------------------> |                  |
       |                  |                      |                  |                     |                  |
       |------------------|                      |------------------|                     |------------------|
                                                                                                   |
                                                             /-------------------------------------/
                          ~/PythonUI/finished.py             |
       this is the end    |------------------|               |
       output.            |                  |               |
       It gives us the    |                  |               |
       differences        |  this is wrong   |        <----- |
                          |  formatting      | 
                          |  technically     | 
                          |  speaking>       | 
                          |                  | 
                          |------------------| 