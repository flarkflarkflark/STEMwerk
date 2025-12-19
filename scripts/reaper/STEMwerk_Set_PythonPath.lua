-- STEMwerk: Set Python Path (ExtState)
-- Lets you point STEMwerk to a specific Python executable (e.g. a ROCm-enabled venv).
--
-- This sets REAPER ExtState section "STEMwerk" key "pythonPath".

local section = "STEMwerk"
local current = reaper.GetExtState(section, "pythonPath")
if current == "" then current = ".venv/bin/python" end

local ok, input = reaper.GetUserInputs("STEMwerk - Python Path", 1, "pythonPath:", current)
if not ok then return end

input = (input or ""):gsub("^%s+", ""):gsub("%s+$", "")
if input == "" then
  reaper.ShowMessageBox("No path entered; nothing changed.", "STEMwerk", 0)
  return
end

reaper.SetExtState(section, "pythonPath", input, true)
reaper.ShowMessageBox("Saved STEMwerk pythonPath:\n\n" .. input .. "\n\nRe-run STEMwerk.", "STEMwerk", 0)


