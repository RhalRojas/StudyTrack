from django.contrib import admin
from .models import Subject, Task, StudySession

admin.site.register(Subject)
admin.site.register(Task)
admin.site.register(StudySession)
