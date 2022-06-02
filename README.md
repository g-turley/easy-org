# Easy-Org

The purpose of Easy-Org is to provide a way for non-technical users to utilize org capture templates and the org-roam database in order to do task management.

## Good to Know Information
The ```./app/org``` folder contains the files generated during the course of using Easy-Org, and from where org-roam will build a database based on the files contained.

The ```./emacs``` folder contains the org capture templates used and the configuration that will be appended temporarily to the user's Doom config. It also contains a README on how to build HTML forms from templates and valid org template expansion variables handled by Easy-Org.

## Requirement

See requirements.txt for updates.

```sh
requests==2.27.1
fastapi==0.72.0
uvicorn==0.17.0
python-dotenv==0.19.2
aiofiles==0.8.0
python-multipart==0.0.5
jinja2==3.0.3
Markdown==3.3.6
pytest==6.2.5
```

Additionally, requires the installation of the following:
* [Doom Emacs](https://github.com/doomemacs/doomemacs)
* [Org-Mode](https://orgmode.org/org.html#Installation)
* [Org-Roam](https://github.com/org-roam/org-roam)
* [Org-Protocol](https://orgmode.org/worg/org-contrib/org-protocol.html)

## Installation & Usage

Clone repo

```bash
$ cd easy-org
# install packages
$ pip install -r requirements.txt
# start the server
$ ./start.sh
```

Visit [http://127.0.0.1:8080/](http://127.0.0.1:8080/).

## The Easy-Org Flow

### GUI Users
* Start the server
    * Org-Roam database is rebuilt
* Open up the 'localhost:8080' webpage
	* HTML Modals are generated, based on the org capture templates, by the create_org_form functions in main.py
* Click on 'New Task'
	* HTML Modal pops up
* Fill out information in form and submit
	* Form values are substituted in a loaded form of the org capture template for 'task', the modified template is sent to org-protocol as the body
	* Org-protocol triggers the org capture template creation via emacsclient for an 'Easy-Org GUI Task' template specified in the modified Doom configs
	* Leftover template expansion variables are substituted
	* Org capture template generates a task in the 'org/task' directory.
* Webpage returns to files

### Emacs Users
* Start the server
	* Org-Roam database is rebuilt
* Run M-x org-capture (SPC X)
* Select an Easy-Org template
* Fill in prompts

# Forked From
[https://shinichiokada.medium.com/](https://shinichiokada.medium.com/) ([Building a Website Starter with FastAPI](https://levelup.gitconnected.com/building-a-website-starter-with-fastapi-92d077092864)).

# License
【MIT License】

Copyright 2022 Garrett Turley, Shinichi Okada

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.