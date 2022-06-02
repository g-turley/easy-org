(org-roam-db-sync)
; Create an org-roam ID every time we run an org capture template.
(add-hook 'org-capture-mode-hook #'org-id-get-create)

; Helper functions
;; Generate list of projects in org-roam db tagged with 'tag', and optionally use org-roam links by setting use-link to boolean true.
(defun easy-org/get-tag-list (tag &optional use-link)
  (if (equal use-link nil)
    (progn (setq taglist (org-roam-db-query (format "select nodes.title from tags inner join nodes on tags.node_id=nodes.id where tags.tag = '\"%s\"'" tag)))
    (push (list tag) taglist)
    (mapconcat #'car taglist "|"))
    (setq link (org-roam-db-query (format "select '\"[[id:' || trim(nodes.id, '\"') ||  '][' || trim(nodes.title, '\"') || ']]\"' from tags inner join nodes on tags.node_id=nodes.id where tags.tag = '\"%s\"'" tag)))
    (push (list tag) link)
    (mapconcat #'car link "|")))

;; Open file handler (required for using function in org-capture templates)
(defun easy-org/get-org-file (name)
  (let ((filename name))
    (set-buffer (find-file-noselect filename))
    (goto-char (point-min))))

;; Sends replaced prompt text to org-protocol (using body variable) as the template.
(defun easy-org/generate-gui-template ()
  (plist-get org-store-link-plist :initial))

;; Generate filenames for template files.
(defun easy-org/get-encode-name ()
  (base64-encode-string (concat (format-time-string "%Y%m%d%H%M%S%N") user-full-name)))

;; Org Capture Functions (cannot have an argument)
(defun easy-org/generate-project-note-name ()
  (setq easy-org-org-note--name (easy-org/get-encode-name))
  (setq easy-org-org-note--directory (concat org-roam-directory "projects"))
  (easy-org/get-org-file (expand-file-name (format "%s.org" easy-org-org-note--name) easy-org-org-note--directory)))

(defun easy-org/generate-task-note-name ()
  (setq easy-org-org-note--name (easy-org/get-encode-name))
  (setq easy-org-org-note--directory (concat org-roam-directory "tasks"))
  (easy-org/get-org-file (expand-file-name (format "%s.org" easy-org-org-note--name) easy-org-org-note--directory)))

(defun easy-org/generate-target-note-name ()
  (setq easy-org-org-note--name (easy-org/get-encode-name))
  (setq easy-org-org-note--directory (concat org-roam-directory "targets"))
  (easy-org/get-org-file (expand-file-name (format "%s.org" easy-org-org-note--name) easy-org-org-note--directory)))

(defun easy-org/generate-checklist-note-name ()
  (setq easy-org-org-note--name (easy-org/get-encode-name))
  (setq easy-org-org-note--directory (concat org-roam-directory "checklists"))
  (easy-org/get-org-file (expand-file-name (format "%s.org" easy-org-org-note--name) easy-org-org-note--directory)))

; Templates
(after! org-roam
  (setq org-capture-templates
             '(("gt" "Easy-org Gui Task" plain
               (function easy-org/generate-task-note-name)
               (function easy-org/generate-gui-template)
               :immediate-finish t)
               ("gp" "Easy-org Gui Project" plain
               (function easy-org/generate-project-note-name)
               (function easy-org/generate-gui-template)
               :immediate-finish t)
               ("gg" "Easy-org Gui Target" plain
               (function easy-org/generate-target-note-name)
               (function easy-org/generate-gui-template)
               :immediate-finish t)
               ("gc" "Easy-org Gui Checklist" plain
               (function easy-org/generate-checklist-note-name)
               (function easy-org/generate-gui-template)
               :immediate-finish t)
               ; Native Emacs Templates
               ("p" "Easy-org Project" plain
               (function easy-org/generate-project-note-name)
               (file "~/Projects/Emacs/easy-org/emacs/project_template.org"))
               ("t" "Easy-org Task" plain
               (function easy-org/generate-task-note-name)
               (file "~/Projects/Emacs/easy-org/emacs/task_template.org"))
                ("g" "Easy-org Target" plain
               (function easy-org/generate-target-note-name)
               (file "~/Projects/Emacs/easy-org/emacs/target_template.org"))
                ("c" "Easy-org Checklist" plain
               (function easy-org/generate-checklist-note-name)
               (file "~/Projects/Emacs/easy-org/emacs/checklist_template.org")))))
