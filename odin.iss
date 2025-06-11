[Setup]
AppName=Odin 프로그램
AppVersion=1.0.0
DefaultDirName={pf}\OdinApp
DefaultGroupName=Odin 프로그램
OutputDir=output
OutputBaseFilename=Odin_Installer
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\odin_2번.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Odin 프로그램"; Filename: "{app}\odin_2번.exe"

[Run]
Filename: "{app}\odin_2번.exe"; Description: "Odin 실행"; Flags: nowait postinstall skipifsilent
