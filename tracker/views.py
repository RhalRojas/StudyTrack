from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Subject, Task, StudySession


def dashboard(request):
    subjects = Subject.objects.all()
    context = {"subjects": subjects}
    return render(request, "tracker/dashboard.html", context)


def task_list(request):
    tasks = Task.objects.select_related("subject").all()
    return render(request, "tracker/task_list.html", {"tasks": tasks})


def log_session(request):
    subjects = Subject.objects.all()

    if request.method == "POST":
        subject = get_object_or_404(Subject, id=request.POST["subject"])
        StudySession.objects.create(
            subject=subject,
            date=request.POST["date"],
            hours=request.POST["hours"],
            notes=request.POST.get("notes", ""),
        )
        messages.success(request, "Session logged.")
        return redirect("dashboard")

    return render(request, "tracker/log_session.html", {"subjects": subjects})
