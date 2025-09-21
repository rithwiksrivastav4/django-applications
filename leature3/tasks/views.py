from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

'''
# Default data
default_tasks = [
    {'name': "rithwik", 'age': 25},
    {'name': "srivastav", 'age': 24},
    {'name': 'bobby', 'age': 10},
    {'name': 'raju', 'age': 9},
    {'name': 'nikhil', 'age': 18},
    {'name': 'varshith', 'age': 17},
]
'''

# ---------------- Forms ----------------
class NewTaskForm(forms.Form):
    task = forms.CharField(label="New member")
    age = forms.IntegerField(label="Age", min_value=1, max_value=130)

class DeleteTaskForm(forms.Form):
    name = forms.CharField(label="Name to delete")

# ---------------- Views ----------------
def tasks_view(request):
    context = {'page': 'view'}
    # Initialize session tasks if not present
    if "tasks" not in request.session:
        request.session["tasks"] = []

    return render(request, "tasks/index.html", context = {
        "tasks": request.session["tasks"],
        "add_form": NewTaskForm(),
        "delete_form": DeleteTaskForm()
    })


def add(request):
    context = {'page': 'addtask'}
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["task"]
            age = form.cleaned_data["age"]

            tasks = request.session.get("tasks", [])
            tasks.append({'name': name, 'age': age})
            request.session["tasks"] = tasks

            return HttpResponseRedirect(reverse("tasks:task"))

    # If GET or invalid, re-render form
    return render(request, "tasks/add.html", context = {"form": NewTaskForm()})


def delete(request):
    context = {'page': 'delete'}
    if request.method == "POST":
        form = DeleteTaskForm(request.POST)
        if form.is_valid():
            name_to_delete = form.cleaned_data["name"]

            tasks = request.session.get("tasks", [])
            tasks = [t for t in tasks if t["name"].lower() != name_to_delete.lower()]

            request.session["tasks"] = tasks
            return HttpResponseRedirect(reverse("tasks:task"))

    # GET → show delete form
    return render(request, "tasks/delete.html",context = {"form": DeleteTaskForm()})
