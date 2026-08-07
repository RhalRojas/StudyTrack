from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Subject, Task, StudySession
from .utils import calculate_priority_score, get_subject_stats, invalidate_subject_stats


def dashboard(request):
    subjects = Subject.objects.all()
    subject_stats = []

    for subject in subjects:
        stats = get_subject_stats(subject)
        subject_stats.append({"subject": subject, **stats})

    upcoming_tasks = Task.objects.filter(is_done=False)
    ranked_tasks = sorted(upcoming_tasks, key=calculate_priority_score, reverse=True)

    context = {
        "subject_stats": subject_stats,
        "ranked_tasks": ranked_tasks[:5],
    }
    return render(request, "tracker/dashboard.html", context)


def task_list(request):
    tasks = list(Task.objects.select_related("subject").all())
    for task in tasks:
        task.priority_score = calculate_priority_score(task)
    tasks.sort(key=lambda t: t.priority_score, reverse=True)
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
        invalidate_subject_stats(subject)
        messages.success(request, "Session logged.")
        return redirect("dashboard")

    return render(request, "tracker/log_session.html", {"subjects": subjects})
