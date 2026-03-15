[Setup]
AppName=Stock Scanner Pro
AppVersion=0.1.0
DefaultDirName={autopf}\Stock Scanner Pro
DefaultGroupName=Stock Scanner Pro
OutputDir=dist
OutputBaseFilename=stock-scanner-setup
Compression=lzma
SolidCompression=yes

[Tasks]
Name: "desktopicon"; Description: "Crear acceso directo en el escritorio"; GroupDescription: "Accesos directos:"; Flags: unchecked

[Files]
Source: "dist\stock-scanner-launcher.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Stock Scanner Pro"; Filename: "{app}\stock-scanner-launcher.exe"
Name: "{autodesktop}\Stock Scanner Pro"; Filename: "{app}\stock-scanner-launcher.exe"; Tasks: desktopicon
