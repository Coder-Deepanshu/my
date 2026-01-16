from django.utils.timezone import now as django_now
from datetime import timedelta, datetime
from .models import QR_code, Leave, Faculty_and_Admin_Attedance, Admin, Faculty
from .redis_client import redis_client
from .serializers import LeaveSerializer

def process_qr_and_leaves():
    # Redis lock (duplicate run se bachne ke liye)
    if redis_client.get("qr_job_running"):
        return
    redis_client.setex("qr_job_running", 300, 1)  # 5 min lock

    print("🔄 Background job started")
    current_datetime = django_now()
    current_date = current_datetime.date()
    current_time = current_datetime.time()

    limit_days = current_date - timedelta(days=3)
    
    # 1️⃣ QR expire check
    expired_qrs = QR_code.objects.filter(
        date=str(current_date),
        expired=True, 
        processed=False
    )

    if not expired_qrs.exists():
        print("✅ No expired QR codes to process")
        return

    def process_user(college_id, user_type):
        """Common function to process both Admin and Faculty"""
        try:
            # Check existing attendance
            existing_attendance = Faculty_and_Admin_Attedance.objects.filter(
                collegeID=college_id, 
                date=current_date
            )
            
            # Process pending attendance from previous days
            pending_attendance = Faculty_and_Admin_Attedance.objects.filter(
                collegeID=college_id, 
                status='Pending', 
                date__lte=limit_days,
                type=user_type
            )
            
            # Process pending leaves from previous days
            pending_leaves = Leave.objects.filter(
                college_id=college_id, 
                end_date__lte=limit_days, 
                status='Pending'
            )
            
            # Auto-reject old pending leaves
            for pending_leave in pending_leaves:
                pending_attendance.update(status='Absent')
                pending_leave.status = 'Rejected'
                pending_leave.rejection_reason = "Admin Doesn't See your Leave!"
                pending_leave.save()
                print(f"Auto-rejected pending leave for {college_id}")
            
            # Create attendance if doesn't exist
            if not existing_attendance.exists():
                leave = Leave.objects.filter(
                    college_id=college_id,
                    start_date__lte=current_date,
                    end_date__gte=current_date  # Changed from __gt to __gte for inclusive range
                ).first()
                
                if leave:
                    status = leave.status
                    leave_type = leave.leave_type
                    leave_time = leave.leave_time or 0.0
                    
                    if status == 'Approved':
                        Faculty_and_Admin_Attedance.objects.create(
                            collegeID=college_id,
                            status='Leave',
                            type=user_type,
                            timing=current_time,
                            date=current_date,
                            leave_time=float(leave_time)
                        )
                    elif status == 'Rejected':
                        Faculty_and_Admin_Attedance.objects.create(
                            collegeID=college_id,
                            status='Absent',
                            type=user_type,
                            timing=current_time,
                            date=current_date,
                            leave_time=float(leave_time)
                        )
                    elif status == 'Pending':
                        if leave_type == 'Emergency Leave':
                            Faculty_and_Admin_Attedance.objects.create(
                                collegeID=college_id,
                                status='Leave',
                                type=user_type,
                                timing=current_time,
                                date=current_date,
                                leave_time=float(leave_time)
                            )
                            # Update leave status to Approved
                            leave.status = 'Approved'
                            leave.save()
                            print(f"Auto-approved emergency leave for {college_id}")
                        elif leave_type in ['Short Leave', 'Planned Leave']:
                            Faculty_and_Admin_Attedance.objects.create(
                                collegeID=college_id,
                                status='Pending',
                                type=user_type,
                                timing=current_time,
                                date=current_date,
                                leave_time=float(leave_time)
                            )
                else:
                    # No leave applied, mark as absent
                    Faculty_and_Admin_Attedance.objects.create(
                        collegeID=college_id,
                        status='Absent',
                        type=user_type,
                        timing=current_time,
                        date=current_date,
                        leave_time=0.0
                    )
            
            return True
        except Exception as e:
            print(f'❌ Error processing {user_type} {college_id}: {str(e)}')
            return False

    # Process all admins
    admin_ids = Admin.objects.values_list('college_id', flat=True)
    for admin_id in admin_ids:
        process_user(admin_id, 'Admin')
    
    # Process all faculty
    faculty_ids = Faculty.objects.values_list('college_id', flat=True)
    for faculty_id in faculty_ids:
        process_user(faculty_id, 'Faculty')
    
    # Mark QR codes as processed
    expired_qrs.update(processed=True)
    
    print("✅ Background job completed")