# Tracta

A causual casual space-themed game where you pull on space debris to escape an endless space
junkyard.

## Build

### Windows

Run the Windows build specification `windows.spec` through PyInstaller

    python -m PyInstaller windows.spec

This should generate an executable in the directory `dist/tracta`. You can delete `.../build` and
any other development files or folders from this directory without compromising the application.