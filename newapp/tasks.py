from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Faculty_and_Admin_Attedance, Leave

@shared_task
def finalize_attendance(attendance_date, college_id):
    print("Celery Task Started")
    print(f"Date: {attendance_date}")
    print(f"college ID: {college_id}")
    attendances = Faculty_and_Admin_Attedance.objects.filter(
        date=attendance_date,
        status='Pending',
    )
    print(f"Total pending: {attendances.count()}")

    for att in attendances:
        print(att.collegeID)
        leave = Leave.objects.filter(
            college_id=att.collegeID,
            start_date__lte = attendance_date,
            end_date__gte = attendance_date
        ).first()

        if leave:
            if leave.status == 'Approved':
                att.status = 'Leave'
                print("Leave Marked")
            else:
                # REJECTED or still PENDING
                att.status = 'Absent'
                print("Absent Marked")
        else:
            att.status = 'Absent'

        att.save()
