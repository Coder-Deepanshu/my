from django.contrib import admin
from .models import Student,Course,Attendance,FeeStructure
from .models import Department, Position, StudentDocuments

from .models import DeviceFingerprint, UserDetail, OTPVerification

@admin.register(OTPVerification)
class OTPVerification(admin.ModelAdmin):
    list_display = ('user', 'otp_code')
    search_fields = ('user',)

@admin.register(UserDetail)
class UserDetail(admin.ModelAdmin):
    list_display = ('username', 'user_id')
    search_fields = ('username',)

@admin.register(DeviceFingerprint)
class DeviceFingerprint(admin.ModelAdmin):
    list_display = ('user', 'fingerprint')
    search_fields = ('user',)


@admin.register(Attendance)
class AttendenceAddAdmin(admin.ModelAdmin):
    list_display = ('college_id', 'status', 'date', 'timing', 'leave_time')
    search_fields = ('college_id', 'status', 'date', 'timing', 'leave_time')




from .models import ChatRoom,Message

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'participant1','participant2']
    
@admin.register(Message)
class Message_Student_faculty(admin.ModelAdmin):
    list_display=('chat_room','sender_id','content')
    search_fields=('chat_room','sender_id',)







# FOR SUPERADMIN
from .models import SuperAdmin
@admin.register(SuperAdmin)
class SuperAdmin(admin.ModelAdmin):
    list_display = ('college_id', "name", "last_name", "username", "password")
    search_fields = ('college_id', "name", "last_name", "username", "password")

# FOR STAFF
from .models import Staff
@admin.register(Staff)
class Staff(admin.ModelAdmin):
    list_display = ('college_id', "name", "last_name", "email", "phone")
    search_fields = ('name', 'college_id',)

# FOR STUDENT
@admin.register(Student)
class Student(admin.ModelAdmin):
    list_display = ('name', 'college_id', 'course')
    search_fields = ('name', 'college_id', 'course')

# FOR STAFF DOCUMENT
# from .models import StaffDocument
# @admin.register(StaffDocument)
# class StaffDocument(admin.ModelAdmin):
#     list_display = ('name', 'college_id', 'course')
#     search_fields = ('name', 'college_id', 'course')

# # FOR STUDENT DOCUMENT
# from .models import StudentDocuments
# @admin.register(StudentDocuments)
# class StudentDocument(admin.ModelAdmin):
#     list_display = ('name', 'college_id', 'course')
#     search_fields = ('name', 'college_id', 'course')

# FOR DEPARTMENT
@admin.register(Department)
class Department(admin.ModelAdmin):
    list_display = ('id', 'name','code', 'type', 'description', 'programs', 'status', 'created_at', 'updated_at')
    search_fields = ('name','code', 'type', 'description', 'programs', 'status', 'created_at', 'updated_at')

# FOR COURSE
@admin.register(Course)
class Course(admin.ModelAdmin):
    list_display=('id', 'image', 'name', 'code', 'level', 'type', 'description', 'fees', 'semesters', 'max_student', 'eligibility', 'created_at', 'updated_at', 'status')
    search_fields=('image', 'name', 'code', 'level', 'type', 'description', 'fees', 'semesters', 'max_student', 'eligibility', 'created_at', 'updated_at', 'status')

# FOR POSITION
@admin.register(Position)
class Position(admin.ModelAdmin):
    list_display = ('id', 'name', 'role', 'type', 'responsibility', 'rank', 'salary', 'status', 'created_at', 'updated_at')
    search_fields = ('name', 'role', 'type', 'responsibility', 'rank', 'salary', 'status', 'created_at', 'updated_at')

# FOR HISTORY
from .models import History
@admin.register(History)
class History(admin.ModelAdmin):
    list_display=('content','updatedFrom','updatedTo')
    search_fields=('content',)

# FOR SUBJECT AND CONTENT
from .models import Subject
@admin.register(Subject)
class Subject(admin.ModelAdmin):
    list_display = ('id', 'course', 'name', 'code', 'semester', 'department', 'content')
    fields=('course', 'name', 'code', 'semester', 'department', 'content')

# FOR LAB
from .models import Lab
@admin.register(Lab)
class Lab(admin.ModelAdmin):
    list_display = ['id', 'name', 'number']
    fields = ['name', 'number']

# FOR LECTURE
from .models import Lecture
@admin.register(Lecture)
class Lecture(admin.ModelAdmin):
    list_display = ['id', 'name', 'course', 'semester', 'type', 'start_time', 'end_time']
    fields = ['name', 'course', 'semester', 'type', 'start_time', 'end_time']

# FOR SCHEDULE
from .models import Schedule
@admin.register(Schedule)
class Schedule(admin.ModelAdmin):
    list_display = ['id', 'lecture', 'faculty', 'subject', 'lab', 'day_name', 'available']
    fields = ['lecture', 'faculty', 'subject', 'lab', 'day_name', 'available']
    
# FOR FEE STRUCTURE
from .models import FeeStructure
@admin.register(FeeStructure)
class FeeStructure(admin.ModelAdmin):
    list_display = ["id", "course", "semester", "due_date", "date"]
    fields = ["course", "semester", "due_date"]

# FOR PAYMENT
from .models import Payment
@admin.register(Payment)
class Payment(admin.ModelAdmin):
    list_display = ["id", "student", "structure", "paid", "date", "method", "transaction_id", "receipt_number", "verified_by", "remarks"]
    fields = ["student", "structure", "paid", "date", "method", "transaction_id", "receipt_number", "verified_by", "remarks"]








from .models import QR_code
@admin.register(QR_code)
class QR_Code(admin.ModelAdmin):
    list_display = ('date', 'time', 'timestamp', 'token', 'random_data', 'expired', 'processed')
    fields = ('timestamp', 'token', 'random_data', 'expired', 'processed')

from .models import Faculty_and_Admin_Attedance
@admin.register(Faculty_and_Admin_Attedance)
class Faculty_and_Admin_Attendance_System(admin.ModelAdmin):
    list_display = ['collegeID', 'status', 'type', 'timing', 'date', 'leave_time']
    fields = ['collegeID', 'status', 'type', 'timing', 'date', 'leave_time']

from .models import Leave
@admin.register(Leave)
class Leave(admin.ModelAdmin):
    list_display = ['id', 'college_id', 'leave_type', 'subject', 'start_date', 'end_date', 'total_days', 'contact_during_leave', 'reason', 'status', 'rejection_reason']
    fields = ['college_id', 'leave_type', 'subject', 'start_date', 'end_date', 'total_days', 'contact_during_leave', 'reason', 'status', 'rejection_reason']



