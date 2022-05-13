import os
import markdown
import requests
from urllib import parse

class OrgFile:
    def __init__(self, filepath):
        self.filepath = filepath
        with open(filepath, "r", encoding="utf-8") as input_file:
            orglines = input_file.readlines()
            # for line in orglines:
            #     if line.startswith(":PROPERTIES:")
    
    def __repr__(self):
        return self.filepath


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

def openorg(filename):
    filepath = os.path.join("app/org/", filename)
    orgfile = OrgFile(filepath)
    # Get properties from file
    data = {
        "text": orgfile
    }
    return data

def org_protocol(request, content):
    body = parse.encoded(content)
    org_link = f"org-protocol://capture?template=w&url=localhost&title=Fake%20atitle&body={body}"
    test_get_response = requests.get(org_link)
    print(test_get_response)
    if test_get_response.status_code == 200:
        print(test_get_response.content.decode('utf-8'))
        # print(json.loads(test_get_response.content.decode('utf-8')))
