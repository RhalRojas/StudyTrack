Instructions on how to run StudyTrack

Testing priority score and streak calculation logic:

1. sudo docker compose exec web python manage.py shell
2. s = Subject.objects.create(name="Test Subject")
   t = Task.objects.create(subject=s, title="Test Task", deadline=date.today() + timedelta(days=3), estimated_effort=4)

   calculate_priority_score(t)   
   calculate_streak(s)           
