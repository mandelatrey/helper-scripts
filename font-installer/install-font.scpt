tell application "System Events"
    delay 8
    tell application "Font Book"
        activate
        delay 8
        tell process "Font Book"
            click button "Install Font" of window 1
        end tell
    end tell
end tell