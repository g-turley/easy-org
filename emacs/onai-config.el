(org-roam-db-sync)
; Create an org-roam ID every time we run an org capture template.
(add-hook 'org-capture-mode-hook #'org-id-get-create)

; Helper functions
;; Generate list of projects in org-roam db tagged with 'tag'.
(defun onai/get-tag-list (tag)
  (setq taglist (org-roam-db-query (format "select nodes.title from tags inner join nodes on tags.node_id=nodes.id where tags.tag = '\"%s\"'" tag)))
  (push (list tag) taglist)
  (mapconcat #'car taglist "|"))

;; Open file handler (required for using function in org-capture templates)
(defun onai/get-org-file (name)
  (let ((filename name))
    (set-buffer (find-file-noselect filename))
    (goto-char (point-min))))

;; Sends replaced prompt text to org-protocol (using body variable) as the template.
(defun onai/generate-gui-template ()
  (plist-get org-store-link-plist :initial))

;; Generate filenames for template files.
(defun onai/get-encode-name ()
  (base64-encode-string (concat (format-time-string "%Y%m%d%H%M%S%N") user-full-name)))

;; Org Capture Functions (cannot have an argument)
(defun onai/generate-project-note-name ()
  (setq onai-org-note--name (onai/get-encode-name))
  (setq onai-org-note--directory (concat org-roam-directory "projects"))
  (onai/get-org-file (expand-file-name (format "%s.org" onai-org-note--name) onai-org-note--directory)))

(defun onai/generate-task-note-name ()
  (setq onai-org-note--name (onai/get-encode-name))
  (setq onai-org-note--directory (concat org-roam-directory "tasks"))
  (onai/get-org-file (expand-file-name (format "%s.org" onai-org-note--name) onai-org-note--directory)))

(defun onai/generate-target-note-name ()
  (setq onai-org-note--name (onai/get-encode-name))
  (setq onai-org-note--directory (concat org-roam-directory "targets"))
  (onai/get-org-file (expand-file-name (format "%s.org" onai-org-note--name) onai-org-note--directory)))

(defun onai/generate-checklist-note-name ()
  (setq onai-org-note--name (onai/get-encode-name))
  (setq onai-org-note--directory (concat org-roam-directory "checklists"))
  (onai/get-org-file (expand-file-name (format "%s.org" onai-org-note--name) onai-org-note--directory)))

; Templates
(after! org-roam
  (setq org-capture-templates
             '(("gt" "Onai Gui Task" plain
               (function onai/generate-task-note-name)
               (function onai/generate-gui-template)
               :immediate-finish t)
               ("gp" "Onai Gui Project" plain
               (function onai/generate-project-note-name)
               (function onai/generate-gui-template)
               :immediate-finish t)
               ("gg" "Onai Gui Target" plain
               (function onai/generate-target-note-name)
               (function onai/generate-gui-template)
               :immediate-finish t)
               ; Native Emacs Templates
               ("p" "Onai Project" plain
               (function onai/generate-project-note-name)
               (file "~/Projects/Emacs/easy-org/emacs/project_template.org"))
               ("t" "Onai Task" plain
               (function onai/generate-task-note-name)
               (file "~/Projects/Emacs/easy-org/emacs/task_template.org"))
                ("g" "Onai Target" plain
               (function onai/generate-target-note-name)
               (file "~/Projects/Emacs/easy-org/emacs/target_template.org"))
                ("c" "Onai Checklist" plain
               (function onai/generate-checklist-note-name)
               (file "~/Projects/Emacs/easy-org/emacs/checklist_template.org")))))
