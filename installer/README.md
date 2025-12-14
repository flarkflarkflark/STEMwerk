# Installer builds (CI)

These are **packaging helpers** so you can download installers from GitHub and test on Windows/macOS/Linux.

## Outputs

- Windows: `STEMwerk-Setup-<version>.exe` (Inno Setup)
- macOS: `STEMwerk-<version>.pkg` (pkgbuild)
- Linux: `stemwerk_<version>_amd64.deb` (dpkg-deb)

## Install locations

- Windows: `%USERPROFILE%\\Documents\\STEMwerk`
- macOS: `/Users/Shared/STEMwerk`
- Linux: `/usr/share/stemwerk`

The REAPER Lua scripts live under `scripts/reaper/` inside the installed folder.

## Building locally

### Windows
- Install Inno Setup (ISCC)
- Run ISCC on `installer/windows/STEMwerk.iss`

### macOS
- `STEMWERK_VERSION=0.0.0 bash installer/macos/build_pkg.sh`

### Linux (Debian/Ubuntu)
- `sudo apt-get install -y rsync dpkg-dev`
- `STEMWERK_VERSION=0.0.0 bash installer/linux/build_deb.sh`
