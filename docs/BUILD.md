# Build (PyInstaller)

Uwaga: w tym repo są przygotowane skrypty buildowania, ale same binarki (`.exe`, `.app`) musisz wygenerować lokalnie lub w CI.

## Windows (`control_center.exe`)
```powershell
.\build\desktop\windows\build.ps1
```
Wynik: `desktop-qt/dist/control_center.exe`

## macOS (`Control_Center.app`)
```bash
./build/desktop/macos/build.sh
```
Wynik: `desktop-qt/dist/Control_Center.app`

