import os.path

from config import BASEDIR
from config import WHITE_SPACE

def generate_index_template(model_name, model_components):
    model_name = model_name.lower()
    template_path = os.path.join(BASEDIR, 'app/templates/' + model_name + '.html')
    template_file = open(template_path, 'w')
    template_file.write("{% extends \"base.html\" %}\n")
    template_file.write("{% block content %}\n")
    template_file.write("\t\t<h1>List of " + model_name.title() + " Entries.</h1>\n")
    template_file.write("\t\t<table id=\"list-view\">\n")
    template_file.write("\t\t\t<thead>\n")
    template_file.write("\t\t\t\t<tr>\n")
    template_file.write("\t\t\t\t\t<td><b>ID</td>\n")

    for component in model_components:
        template_file.write("\t\t\t\t\t<td><b>" + component['field_name'].title() + "</b></td>\n")

    template_file.write("\t\t\t\t\t<td><b> </td>\n")
    template_file.write("\t\t\t\t\t<td><b> </td>\n")
    template_file.write("\t\t\t\t</tr>\n")
    template_file.write("\t\t\t</thead>\n")
    template_file.write("\t\t\t{% if " + model_name + "_entries %}\n")
    template_file.write("\t\t\t<tbody>\n")
    template_file.write("\t\t\t{% for entry in " + model_name + "_entries %}\n")
    template_file.write("\t\t\t\t<tr>\n")
    template_file.write("\t\t\t\t\t<td><a href=\"/"+model_name+"/{{ entry.id }}\">{{ entry.id }}</a></td>\n")

    for component in model_components:
        template_file.write("\t\t\t\t\t<td>{{ entry." + component['field_name'] + " }}</td>\n")

    template_file.write('\t\t\t\t\t<td><a href="/' + model_name + '/edit/{{ entry.id }}">Edit</a></td>\n')
    template_file.write('\t\t\t\t\t<td><a id="delete-link" data-callback="/' + model_name + '/" data-url="/' + model_name + '/{{ entry.id }}">Delete</a></td>\n')
    template_file.write("\t\t\t\t</tr>\n")
    template_file.write("\t\t\t{% endfor %}\n")
    template_file.write("\t\t\t</tbody>\n")
    template_file.write("\t\t</table>\n")
    template_file.write("\t\t\t{% else %}\n")
    template_file.write("\t\t</table>\n")
    template_file.write("\t\tYou have no entries yet\n")
    template_file.write("\t\t\t{% endif %}\n")
    template_file.write('\t\t\t<br/><br/><b><a id="actions" href="/' + model_name + '/add">Add new entry</a></b>\n')
    template_file.write("{% endblock %}\n")

    print "index template generated"

def generate_view_template(model_name, model_components):
    model_name = model_name.lower()
    template_path = os.path.join(BASEDIR, 'app/templates/' + model_name + '_view.html')
    template_file = open(template_path, 'w')
    template_file.write("{% extends \"base.html\" %}\n")
    template_file.write("{% block content %}\n")
    template_file.write("\t\t<h1>View " + model_name.title() + " single entry.</h1>\n")
    template_file.write("\t\t<table>\n")

    for component in model_components:
        template_file.write("\t\t\t\t<tr>\n")
        template_file.write("\t\t\t\t\t<td>" + component['field_name'].title() + ":</td>\n")
        template_file.write("\t\t\t\t\t<td>{{ " + model_name + "." + component['field_name'].lower() + " }}</td>\n")
        template_file.write("\t\t\t\t</tr>\n")

    template_file.write("\t\t</table>\n")
    template_file.write("{% endblock %}")

    print 'view template generated'

def generate_edit_template(model_name, model_components):
    model_name = model_name.lower()
    controller_path = os.path.join(BASEDIR, 'app/controllers/'+model_name+'.py')
    template_path = os.path.join(BASEDIR, 'app/templates/' + model_name + '_edit.html')

    controller_file = open(controller_path, 'a')
    controller_file.write("@"+model_name+"_view.route('/" + model_name + "/edit/<id>')\n")
    controller_file.write("def " + model_name + "_edit_controller(id):\n")
    controller_file.write(WHITE_SPACE + "#this is the controller to edit model entries\n")
    controller_file.write(WHITE_SPACE + model_name + "_item = " + model_name.title() + ".query.get(id)\n")
    controller_file.write(WHITE_SPACE + "return render_template('" + model_name + "_edit.html', " + model_name + "_item = " + model_name + "_item, title = \"Edit Entries\")\n\n")

    template_file = open(template_path, 'w')
    template_file.write("{% extends \"base.html\" %}\n")
    template_file.write("{% block content %}\n")
    template_file.write("\t\t<h1>Edit " + model_name.title() + " Entries.</h1>\n")
    template_file.write("\t\t<form id=\"edit-form\" name=\"" + model_name + "_add\" method=\"put\" action=\"/" + model_name + "/{{ " + model_name + "_item.id }}\">\n")
    template_file.write("\t\t<input type=\"hidden\" id=\"url\" value=\"/"+model_name+"/{{ " + model_name + "_item.id }}\">\n")
    template_file.write("\t\t<table>\n")

    for component in model_components:
        template_file.write("\t\t\t\t<tr>\n")
        template_file.write("\t\t\t\t\t<td>" + component['field_name'].title() + ":</td>\n")
        template_file.write("\t\t\t\t\t<td><input type=\"text\" name=\"" + component['field_name'].lower() + "\" value=\"{{ " + model_name + "_item." + component['field_name'].lower() + " }}\"/></td>\n")
        template_file.write("\t\t\t\t</tr>\n")

    template_file.write("\t\t\t\t<tr>\n")
    template_file.write("\t\t\t\t\t<td><input id=\"submit-put\" type=\"submit\" name=\"submit\" value=\"Edit Entry\"/></td>\n")
    template_file.write("\t\t\t\t\t<td> </td>\n")
    template_file.write("\t\t\t\t</tr>\n")
    template_file.write("\t\t</table>\n")
    template_file.write("\t\t</form>\n")
    template_file.write("{% endblock %}")

    print 'Entries edit and update form controller added'


def generate_controller_template(model_name, model_components):

    model_name = model_name.lower()
    controller_path = os.path.join(BASEDIR, 'app/controllers/'+model_name+'.py')
    template_path = os.path.join(BASEDIR, 'app/templates/' + model_name + '_add.html')

    controller_file = open(controller_path, 'a')
    controller_file.write("@"+model_name+"_view.route('/" + model_name + "/add/')\n")
    controller_file.write("def " + model_name + "_add_controller():\n")
    controller_file.write(WHITE_SPACE + "#this is the controller to add new model entries\n")
    controller_file.write(WHITE_SPACE + "return render_template('" + model_name + "_add.html', title = \"Add New Entry\")\n\n")

    template_file = open(template_path, 'w')
    template_file.write("{% extends \"base.html\" %}\n")
    template_file.write("{% block content %}\n")
    template_file.write("\t\t<h1>Add new " + model_name.title() + " Entries.</h1>\n")
    template_file.write("\t\t<form name=\"" + model_name + "_add\" method=\"post\" action=\"/" + model_name + "/\">\n")
    template_file.write("\t\t<table>\n")

    for component in model_components:
        template_file.write("\t\t\t\t<tr>\n")
        template_file.write("\t\t\t\t\t<td>" + component['field_name'].title() + ":</td>\n")
        template_file.write("\t\t\t\t\t<td><input type=\"text\" name=\"" + component['field_name'].lower() + "\"/></td>\n")
        template_file.write("\t\t\t\t</tr>\n")

    template_file.write("\t\t\t\t<tr>\n")
    template_file.write("\t\t\t\t\t<td><input type=\"submit\" name=\"submit\" value=\"Add Entry\"/></td>\n")
    template_file.write("\t\t\t\t\t<td> </td>\n")
    template_file.write("\t\t\t\t</tr>\n")
    template_file.write("\t\t</table>\n")
    template_file.write("\t\t</form>\n")
    template_file.write("{% endblock %}")

    print 'Data add form controller generated'


# end of file