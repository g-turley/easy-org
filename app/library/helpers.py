import os
import subprocess
import re
import markdown
import requests
from urllib import parse

class OrgFile:
    def __init__(self, filepath):
        self.filepath = filepath
        self.header = dict()
        self.properties = dict()
        self.items = []
        self.text = ""
        collecting_properties = False
        with open(filepath, "r", encoding="utf-8") as input_file:
            self.orglines = input_file.readlines()
            for line in self.orglines:
                # Item properties
                if ":PROPERTIES:" in line:
                    collecting_properties = True
                    continue
                elif ":END:" in line:
                    collecting_properties = False
                    continue
                # Headers, properties, items
                if collecting_properties:
                    pass
                # Headers
                elif line.startswith("#+"):
                    headerprop = line.split(":")
                    self.header[headerprop[0][2:]] = headerprop[1]
                else:
                    self.text += line

def openfile(filename):
    filepath = os.path.join("app/pages/", filename)
    with open(filepath, "r", encoding="utf-8") as input_file:
        text = input_file.read()

    html = markdown.markdown(text)
    data = {
        "text": html
    }
    return data

def listorg(current_dir="\\"):
    if current_dir != "\\":
        print(current_dir)
        last_dir = current_dir
        link_up = "\\".join(last_dir.split("\\")[:-1])
        if link_up == "":
            link_up = "\\"
    else:
        last_dir = "\\"
        link_up = "\\"
    dir_files = []
    # Not sure if this is necessarily safe
    dir_scan = f".\\app\\org\\{current_dir}"
    dir_scan = dir_scan.replace("\\", os.sep)
    with os.scandir(dir_scan) as it:
        for entry in it:
            if not entry.name.startswith("."):
                if entry.is_dir():
                    dir_files.append(entry.name)
                elif entry.is_file():
                    if entry.name.endswith('.org'):
                        dir_files.append(entry.name)
    data = {
        "files": dir_files,
        "dir": last_dir,
        "link_up": link_up
    }
    return data

def readorg(filename):
    filepath = os.path.join(".\\app\\org\\", filename)
    filepath = filepath.replace("\\", os.sep)
    orgfile = OrgFile(filepath)
    # Get properties from file
    data = {
        "lines": orgfile.orglines
    }
    return data

def get_org_inputs(form_type):
    form_values = dict()
    with open(f'./emacs/{form_type}_template.org', 'r') as t:
        for m in re.finditer(r"%\^{(.+)}(p)*", t.read()):
            default = ""
            options = []
            match_group = m.group(1)
            if match_group.startswith("%("):
                evaluate = subprocess.check_output(f"emacsclient --eval '{match_group[1:]}'", shell=True).decode('utf-8')[1:-2]
                match_group = evaluate
            if "|" in match_group:
                options = match_group.split("|")
                label = options[0]
                default = options[1]
                options = options[2:]
            else:
                label = match_group
            form_values[label] = (m.group(0),m.group(2), default, options)
    return form_values

def create_org_form(form_type):
    form_values = get_org_inputs(form_type)
    with open(f'./templates/forms/{form_type}_form.html', 'w') as f:
        f.write("{% extends './forms/form_base.html' %}")
        f.write("{% set formTitle = '"+ form_type.title() +"' %}")
        f.write("{% block form_content %}")
        # Form submit
        f.write(f'<form action="/org/new?form_type={form_type}" method="post">')
        f.write('<div class="modal-body">')
        for form_element in form_values.keys():
            default = form_values[form_element][-2]
            options = form_values[form_element][-1]
            if len(options) > 0:
                f.write(f'<div class="input-group mb-3"><label class="input-group-text" for="inputGroupSelect{form_element}">{form_element}</label><select class="form-select" name="{form_element}" id="inputGroupSelect{form_element}">')
                if default != "":
                    f.write(f'<option value="{default}" selected>{default}</option>')
                else:
                    f.write(f'<option selected>Choose an option...</option>')
                for option in options:
                    f.write(f'<option value="{option}">{option}</option>')
                f.write('</select></div>')
            else:
                f.write(f'<div class="mb-3"><label for="{form_element}FormControlInput" class="form-label">{form_element.title()}</label>')
                if default != "":
                    default_html = f"value='{default}'"
                else:
                    default_html = ""
                end_input_type = ""
                if form_element == "Description":
                    input_type = "textarea"
                    end_input_type = "</textarea>"
                else:
                    input_type = "input"
                f.write(f'<{input_type} type="text" name="{form_element}" class="form-control" id="{form_element}ControlInput" ' + default_html + f' >{end_input_type}')
                f.write('</div>')
        f.write('</div><div class="modal-footer"><button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button><button type="submit" class="btn btn-primary">Submit</button></div></form>{% endblock %}')

def create_org_template(form_type: str, input_values):
    form_values = dict()
    property_switch = False
    # filename is the first value extracted from the template, that isn't named same as template name.
    filename = ""
    # This variable is for property drawers
    last_group = ""
    with open(f'./emacs/{form_type}_template.org', 'r') as t:
        text = t.read()
        for m in re.finditer(r"%\^{(.+)}(p)*", text):
            match_group = m.group(1)
            if match_group.startswith("%("):
                evaluate = subprocess.check_output(f"emacsclient --eval '{match_group[1:]}'", shell=True).decode('utf-8')[1:-2]
                match_group = evaluate
            if "|" in match_group:
                options = match_group.split("|")
                label = options[0]
                default = options[1]
                options = options[2:]
            else:
                label = match_group
            if filename == "":
                filename = input_values.get(label)
            if m.group(2) == "p":
                # New list of properties
                if not property_switch:
                    org_text = ":PROPERTIES:\n"
                    property_switch = True
                    org_text += f":{label}: {input_values.get(label)}"
                else:
                    org_text = f":{label}: {input_values.get(label)}"
            else:
                # Thing before was a property.
                if property_switch:
                    text = f"{last_group}\n:END:".join(text.rsplit(last_group, 1))
                    property_switch = False
                org_text = input_values.get(label)
            # Only replace one since we are iterating
            text = text.replace(m.group(0), org_text, 1)
            last_group = org_text
        # If there are no more match groups, but our property drawer is open, close it.
        if property_switch:
            text = f"{last_group}\n:END:".join(text.rsplit(last_group, 1))
    return filename, text

def org_protocol(contenttype: str, filename:str, content: str):
    url = contenttype
    title = filename
    if contenttype == "project":
        template = "gp"
    elif contenttype == "task":
        template = "gt"
    elif contenttype == "target":
        template = "gg"
    url = parse.quote(url)
    title = parse.quote(title)
    body = parse.quote(content)
    # Super unsafe, but we expect this.
    # This uses template 't'
    return os.system(f'emacsclient "org-protocol://capture?template={template}&url={url}&title={title}&body={body}"')