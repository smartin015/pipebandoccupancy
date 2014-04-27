Set oShell = CreateObject ("Wscript.Shell") 
Dim strArgs
strArgs = "cmd /c startpy.bat"
oShell.Run strArgs, 0, false