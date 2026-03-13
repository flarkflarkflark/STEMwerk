-- STEMwerk: Smart FFmpeg Setup
-- Automatically finds FFmpeg or guides the user through installation.

local section = "STEMwerk"

local function fileExists(path)
    if not path or path == "" then return false end
    local f = io.open(path, "r")
    if f then f:close(); return true end
    return false
end

local function findFfmpeg()
    -- 1. Try 'where' command (Windows)
    local f = io.popen("where ffmpeg 2>nul")
    if f then
        local res = f:read("*l")
        f:close()
        if res and fileExists(res) then return res end
    end
    
    -- 2. Check common installation paths
    local appdata = os.getenv("LOCALAPPDATA") or ""
    local programFiles = os.getenv("ProgramFiles") or "C:\\Program Files"
    
    local common = {
        programFiles .. "\\ffmpeg\\bin\\ffmpeg.exe",
        "C:\\ffmpeg\\bin\\ffmpeg.exe",
        appdata .. "\\Microsoft\\WinGet\\Links\\ffmpeg.exe",
        "C:\\ProgramData\\chocolatey\\bin\\ffmpeg.exe"
    }
    
    for _, p in ipairs(common) do
        if fileExists(p) then return p end
    end
    return nil
end

local function openDownloadPage()
    local url = "https://www.gyan.dev/ffmpeg/builds/"
    if package.config:sub(1,1) == "\\" then -- Windows
        os.execute('start "" "' .. url .. '"')
    else
        os.execute('open "' .. url .. '"')
    end
end

local function main()
    local found = findFfmpeg()
    
    if found then
        local msg = "FFmpeg is automatisch gevonden op:\n\n" .. found .. "\n\nWilt u dit pad gebruiken voor STEMwerk?"
        local res = reaper.ShowMessageBox(msg, "FFmpeg Gevonden", 4) -- 4 = Yes/No
        if res == 6 then -- Yes
            reaper.SetExtState(section, "ffmpegPath", found, true)
            reaper.ShowMessageBox("Succes! FFmpeg is nu ingesteld.", "STEMwerk", 0)
            return
        end
    end

    -- Not found or user said No
    local msg = "FFmpeg kon niet worden gevonden op uw systeem.\n\n" ..
                "Wat wilt u doen?\n\n" ..
                "JA: Handmatig het pad naar ffmpeg.exe opzoeken\n" ..
                "NEE: FFmpeg downloaden via de website (opent browser)\n" ..
                "CANCEL: Niets doen"
    
    local choice = reaper.ShowMessageBox(msg, "STEMwerk - FFmpeg Setup", 3) -- 3 = Yes/No/Cancel

    if choice == 6 then -- Yes (Manual)
        local current = reaper.GetExtState(section, "ffmpegPath")
        if current == "" then current = "C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe" end
        
        local ok, input = reaper.GetUserInputs("Pad naar ffmpeg.exe", 1, "Bestandspad:,extrawidth=200", current)
        if ok and input ~= "" then
            input = input:gsub('"', '') -- Remove quotes if user copied path with quotes
            if fileExists(input) then
                reaper.SetExtState(section, "ffmpegPath", input, true)
                reaper.ShowMessageBox("Succes! Pad opgeslagen:\n" .. input, "STEMwerk", 0)
            else
                reaper.ShowMessageBox("FOUT: Het bestand bestaat niet op de opgegeven locatie.\n\nZorg dat u naar het .exe bestand verwijst.", "Fout", 0)
                main() -- Retry
            end
        end
    elseif choice == 7 then -- No (Download)
        openDownloadPage()
        reaper.ShowMessageBox("De downloadpagina is geopend in uw browser.\n\n1. Download een 'release build' (bijv. ffmpeg-release-essentials.7z)\n2. Pak het uit\n3. Start dit script opnieuw om het pad naar 'bin/ffmpeg.exe' op te geven.", "Handleiding", 0)
    end
end

main()
