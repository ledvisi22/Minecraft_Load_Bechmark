tell application "System Events"
    set frontApp to name of first application process whose frontmost is true
    set windowTitle to name of first window of application process frontApp
end tell
return windowTitle
