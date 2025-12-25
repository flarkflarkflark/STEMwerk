-- @description Stemwerk: Installation & Setup
-- @author flarkAUDIO
-- @version 2.0.0
-- @changelog
--   Initial guided installer / verifier (cross-platform).
-- @link Repository https://github.com/flarkflarkflark/STEMwerk

local EXT_SECTION = "STEMwerk"

local function msgBox(title, text, type)
    return reaper.ShowMessageBox(tostring(text), tostring(title), type or 0)
end

local function getOS()
    local sep = package.config:sub(1, 1)
    local osName = reaper.GetOS() or ""
    if osName:match("OSX") or osName:match("macOS") then return "macOS" end
    return "Linux"
end

local OS = getOS()

local function getScriptDir()
    local info = debug.getinfo(1, "S")
    return (info and info.source and info.source:match("@?(.*[/\\])")) or ""
end

local function quoteArg(s)
    s = tostring(s)
    if s:find('"') then
        s = s:gsub('"', '\\"')
    end
    if s:find("%s") then
        return '"' .. s .. '"'
    end
    return s
end

local function exec(cmd, timeoutMs)
    timeoutMs = timeoutMs or 30000
    if reaper and reaper.ExecProcess then
        local rc, out = reaper.ExecProcess(cmd, timeoutMs)
        return tonumber(rc) or -1, out or ""
    end
    local ok = os.execute(cmd)
    return (ok == true or ok == 0) and 0 or 1, ""
end

local function fileExists(path)
    local f = io.open(path, "r")
    if f then f:close(); return true end
    return false
end

local function setExt(key, value)
    if reaper and reaper.SetExtState then
        reaper.SetExtState(EXT_SECTION, key, tostring(value), true)
    end
end

    -- TEST: Toon Python-versie in Reaper-console
    local function showPythonVersion()
        local pythonExe = "python" -- gebruik globale python
        local version, output = getPythonVersion(pythonExe)
        reaper.ShowConsoleMsg("Python executable: " .. pythonExe .. "\n")
        reaper.ShowConsoleMsg("Python version: " .. tostring(version) .. "\n")
        reaper.ShowConsoleMsg("Raw output: " .. tostring(output) .. "\n")
    end

    -- Roep de testfunctie aan (voor debug/demo)
    -- Verplaatst naar het einde van het script zodat alle functies beschikbaar zijn


local function getPythonVersion(python)
    local tempFile = os.tmpname() .. ".txt"
    local cmd = quoteArg(python) .. ' -c "import sys; print(sys.version)" > ' .. quoteArg(tempFile)
    local rc = exec(cmd, 15000)
    local out = nil
    if rc == 0 then
        local f = io.open(tempFile, "r")
        if f then
            out = f:read("*a")
            f:close()
            os.remove(tempFile)
        end
    end
    if not out then return nil, nil end
    local v = (out or ""):match("(%d+%.%d+%.%d+)")
    return v, out
end

local function getHome()
    if OS == "Windows" then
        return os.getenv("USERPROFILE") or "C:\\Users\\Default"
    end
    return os.getenv("HOME") or "/tmp"
end

local function detectPython()
    local configured = reaper.GetExtState(EXT_SECTION, "pythonPath")
    if configured ~= "" then
        -- Verify configured python is runnable before trusting it
        local v = nil
        v = (select(1, (function()
            local version = nil
            local cmd = quoteArg(configured) .. ' -c "import sys; print(f\\"{sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}\\")"'
            local rc = select(1, exec(cmd, 12000))
            if rc == 0 then version = "ok" end
            return version
        end)()))
        if v then
            return configured
        end
    end

    local scriptDir = getScriptDir()
    local home = getHome()

    local candidates = {}

    if OS == "Windows" then
        local localAppData = os.getenv("LOCALAPPDATA") or ""
        local programFiles = os.getenv("ProgramFiles") or "C:\\Program Files"
        local programFilesX86 = os.getenv("ProgramFiles(x86)") or "C:\\Program Files (x86)"

        -- Prefer common Python installs
        table.insert(candidates, localAppData .. "\\Programs\\Python\\Python311\\python.exe")
        table.insert(candidates, localAppData .. "\\Programs\\Python\\Python310\\python.exe")
        table.insert(candidates, localAppData .. "\\Programs\\Python\\Python312\\python.exe")

        -- System installs
        table.insert(candidates, programFiles .. "\\Python311\\python.exe")
        table.insert(candidates, programFiles .. "\\Python310\\python.exe")
        table.insert(candidates, programFilesX86 .. "\\Python311\\python.exe")
        table.insert(candidates, programFilesX86 .. "\\Python310\\python.exe")

        -- Windows Store aliases (if enabled)
        table.insert(candidates, localAppData .. "\\Microsoft\\WindowsApps\\python.exe")
        table.insert(candidates, localAppData .. "\\Microsoft\\WindowsApps\\python3.exe")

        -- Repo/portable venv patterns (best-effort)
        table.insert(candidates, scriptDir .. "..\\..\\.venv\\Scripts\\python.exe")
        table.insert(candidates, home .. "\\Documents\\STEMwerk\\.venv\\Scripts\\python.exe")

        -- PATH fallback
        -- Fallback
        table.insert(candidates, "python")
    else
        table.insert(candidates, scriptDir .. "../../.venv/bin/python")
        table.insert(candidates, home .. "/.STEMwerk/.venv/bin/python")
        if OS == "macOS" then
            table.insert(candidates, "/opt/homebrew/bin/python3")
            table.insert(candidates, "/usr/local/bin/python3")
            table.insert(candidates, "/usr/local/opt/python@3.11/bin/python3")
            table.insert(candidates, "/usr/local/opt/python@3.12/bin/python3")
        end
        table.insert(candidates, "/usr/bin/python3")
        table.insert(candidates, "python3")
        table.insert(candidates, "python")
    end

    for _, p in ipairs(candidates) do
        reaper.ShowConsoleMsg("Probeer python pad: " .. tostring(p) .. "\n")
        local v, out = nil, nil
        if p == "python" or p == "python3" then
            v, out = getPythonVersion(p)
        else
            if fileExists(p) then
                v, out = getPythonVersion(p)
            end
        end
        reaper.ShowConsoleMsg("Resultaat versie: " .. tostring(v) .. "\n")
        reaper.ShowConsoleMsg("Exec output: " .. tostring(out) .. "\n")
        if v then return p end
    end

    return OS == "Windows" and "python" or "python3"
end

local function getPythonVersion(python)
    local cmd = quoteArg(python) .. ' -c "import sys; print(f\"{sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}\")"'
    local rc, out = exec(cmd, 15000)
    if rc ~= 0 then return nil, out end
    local v = (out or ""):match("(%d+%.%d+%.%d+)")
    return v, out
end

local function checkFfmpeg()
    local rc = exec("ffmpeg -version", 8000)
    return rc == 0
end

local function getSeparatorScriptPath()
    local configured = reaper.GetExtState(EXT_SECTION, "separatorScript")
    if configured ~= "" then
        return configured
    end
    local scriptDir = getScriptDir()
    return scriptDir .. "audio_separator_process.py"
end

local function runSeparatorCheck(python, separatorScript)
    local cmd = quoteArg(python) .. " " .. quoteArg(separatorScript) .. " --check"
    return exec(cmd, 600000)
end

msgBox("Stemwerk Setup", "This wizard will help you verify Python, audio-separator, and ffmpeg.\n\nIt can also save your detected Python path into REAPER settings.", 0)

local python = detectPython()
local version, versionRaw = getPythonVersion(python)
if not version then
    msgBox("Stemwerk Setup", "Python was not found or not runnable.\n\nRecommended: Python 3.11.\n\nWindows:\n  winget install Python.Python.3.11\n\nmacOS:\n  brew install python@3.11\n\nLinux:\n  Install python3.11 via your package manager.", 0)
    return
end

-- Warn for too-new versions (best-effort compare)
local major, minor = version:match("^(%d+)%.(%d+)")
major, minor = tonumber(major), tonumber(minor)
if major == 3 and minor and minor >= 14 then
    msgBox("Stemwerk Setup", "⚠️ Python 3.14+ is not compatible with audio-separator dependencies yet.\n\nUse Python 3.11 for best compatibility (and AMD DirectML on Windows).\n\nDetected: " .. tostring(version) .. "\nPython: " .. tostring(python), 0)
end

setExt("pythonPath", python)
setExt("separatorScript", getSeparatorScriptPath())

local installText = "Install/upgrade dependencies now?\n\nThis runs:\n  " .. python .. " -m pip install --upgrade pip\n  " .. python .. " -m pip install audio-separator[gpu]\n\n(You can cancel and install manually if you prefer.)"
local doInstall = (msgBox("Stemwerk Setup", installText, 4) == 6)
if doInstall then
    exec(quoteArg(python) .. " -m pip install --upgrade pip", 600000)
    exec(quoteArg(python) .. " -m pip install \"audio-separator[gpu]\"", 600000)
end

if not checkFfmpeg() then
    local ff = "ffmpeg was not found in PATH.\n\nInstall it and retry:\n"
    if OS == "Windows" then
        ff = ff .. "  winget install Gyan.FFmpeg\n"
    elseif OS == "macOS" then
        ff = ff .. "  brew install ffmpeg\n"
    else
        ff = ff .. "  Ubuntu/Debian: sudo apt install ffmpeg\n  Arch: sudo pacman -S ffmpeg\n"
    end
    msgBox("Stemwerk Setup", ff, 0)
end

local separatorScript = getSeparatorScriptPath()
local rc, out = runSeparatorCheck(python, separatorScript)
if rc ~= 0 then
    msgBox("Stemwerk Setup", "Check failed. Output:\n\n" .. tostring(out), 0)
    return
end

msgBox("Stemwerk Setup", "✅ Setup looks OK.\n\nNext:\n- Load script actions (ReaScript: Load...)\n- Add toolbar buttons for the preset scripts if desired.", 0)
