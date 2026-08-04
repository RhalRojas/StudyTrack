from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class StudySession(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="sessions")
    date = models.DateField()
    hours = models.DecimalField(max_digits=4, decimal_places=2)
    notes = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.subject.name} - {self.date} ({self.hours}h)"


class Task(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=200)
    deadline = models.DateField()
    estimated_effort = models.PositiveSmallIntegerField(
        help_text="Rough effort score from 1 (light) to 5 (heavy)"
    )
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.title
