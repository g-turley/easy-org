# Setup Roam directory
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
APP_ROAM="(setq org-roam-directory \"${SCRIPT_DIR}/app/org/\")"
APP_AGENDA="(setq org-agenda-files '(\"${SCRIPT_DIR}/app/org/tasks\"))"
# Setup for app
# Backup Doom Config
cp ~/.doom.d/config.el ~/.doom.d/config.el.bak
# Write Onai Configuration to Doom Config
echo "; Onai Configuration" >> ~/.doom.d/config.el
echo "${APP_ROAM}" >> ~/.doom.d/config.el
echo "${APP_AGENDA}" >> ~/.doom.d/config.el
cat ./emacs/onai-config.el >> ~/.doom.d/config.el # Append our templates to the local Doom config
# Run App
uvicorn app.main:app --reload --port 8080 & emacs --eval "(server-start)" && kill $!
# Restore previous state
cp ~/.doom.d/config.el.bak ~/.doom.d/config.el # Restore Doom Config