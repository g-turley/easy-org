# Easy-Org Templates
All template expansion prompts (```%^{PROMPT}``` and ```%^{PROP}p```) are turned into inputs for the GUI form.
It is permissible to use the %(EXP) template expansion inside of prompts, as well as the use of defaults (ie ```%^{PROMPT|default}```) and multiple options (ie ```%^{PROMPT|default|option1|option2}```).
The name of the prompt or prop can also be used to modify the resulting form. Any prompt ending in 'description' will be turned into a textarea, and a prompt ending in 'date' will offer a datetime picker.

To generate the template call the Python function ```create_org_form(TEMPLATE)``` where TEMPLATE represents the partial name of the template file name in the emacs directory (ie project_template.org would be 'project' or test_template.org would be 'test').
All resulting forms will be generated into the ```../template/forms``` directory.

## Specialized Expressions
### easy-org/get-tag-list
This function will query the org-roam database for files tagged with a specified tag, and either return a string of options (ie ```TAG|option1|option2|option3```) or a string of org-roam links and options (ie ```TAG|[[id:1234-5678-9012-3456][option1]]|[[id:2345-6789-0123-4567][option2]]|[[id:3456-7890-1234-5678][option3]]```).
Example use to return string of options for the tag "Project":

```lisp
%(easy-org/get-tag-list "Project")
```

Example use to return string of org-roam links for the tag "Task":

```lisp
%(easy-org/get-tag-list "Task" t)
```