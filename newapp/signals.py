from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Schedule, Lecture
from datetime import date, timedelta
from .utils import schedule

def daysName(number):
    if number < 1 or number > 7:
        raise ValueError("Days must be between 1 and 7.")

    today = date.today()
    monday = today - timedelta(days=today.weekday())
    days = []

    for i in range(number):
        day_start = monday + timedelta(days=i)
        days.append(day_start.strftime("%A"))

    return days

@receiver(post_save, sender=Lecture)
def create_schedule_slots(sender, instance, created, **kwargs):
    if not created:
        return

    days = daysName(schedule(True))

    schedules = []
    if instance.type != 'interval':
        for day in days:
            if not Schedule.objects.filter(lecture=instance, day_name=day).exists():
                schedules.append(Schedule(lecture=instance, day_name=day, available=True))

        Schedule.objects.bulk_create(schedules)
