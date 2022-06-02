# Setup Roam directory
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
APP_ROAM="(setq org-roam-directory \"${SCRIPT_DIR}/app/org/\")"
APP_AGENDA="(setq org-agenda-files '(\"${SCRIPT_DIR}/app/org/tasks\"))"
# Setup for app
# Backup Doom Config
if [ -d "`eval echo ~/.doom.d/`" ] 
then
    echo "[✓] Doom Emacs is installed." 
else
    echo "[!] Expected the ~/.doom.d/ directory, but it doesn't exist."
    echo "[!] Install Emacs Doom and then re-run this script."
    exit
fi
cp ~/.doom.d/config.el ~/.doom.d/config.el.bak
# Write Configuration to Doom Config
echo "[i] Appending Easy-Org config to Doom config..." 
echo "; Easy-Org Configuration" >> ~/.doom.d/config.el
echo "${APP_ROAM}" >> ~/.doom.d/config.el
echo "${APP_AGENDA}" >> ~/.doom.d/config.el
cat ./emacs/easy-org-config.el >> ~/.doom.d/config.el # Append our templates to the local Doom config
# Run App
echo "[i] Running Easy-Org..." 
uvicorn app.main:app --reload --port 8080 & emacs --eval "(server-start)" && kill $!
# Restore previous state
echo "[i] Restoring Previous Configuration" 
cp ~/.doom.d/config.el.bak ~/.doom.d/config.el # Restore Doom Config