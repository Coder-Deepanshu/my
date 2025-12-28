from django.contrib import admin
from .models import Student,Faculty,Course,Attendance,FeePayment,FeeStructure,Admin,StudentBalance, Subject_Details
from .models import Department,Level,Position, StudentDocuments,AdminDocuments, FacultyDocuments

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

@admin.register(StudentBalance)
class StudentAddAdmin(admin.ModelAdmin):
    list_display = ('student', 'extra_amount')
    search_fields = ('student',)

@admin.register(StudentDocuments)
class StudentDocuments(admin.ModelAdmin):
    list_display = ('student', 'uploaded_at')
    search_fields = ('student',)

@admin.register(FacultyDocuments)
class FacultyDocuments(admin.ModelAdmin):
    list_display = ('faculty', 'uploaded_at')
    search_fields = ('faculty',)
    
@admin.register(AdminDocuments)
class AdminDocuments(admin.ModelAdmin):
    list_display = ('admin', 'uploaded_at')
    search_fields = ('admin',)

@admin.register(Student)
class StudentAddAdmin(admin.ModelAdmin):
    list_display = ('name', 'college_id', 'course')
    search_fields = ('name', 'college_id', 'course')

@admin.register(Attendance)
class AttendenceAddAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'faculty')
    search_fields = ('student', 'course', 'faculty')

@admin.register(Course)
class coursesAdmin(admin.ModelAdmin):
    list_display=('name','no_of_years','no_of_semesters')
    search_fields=('name',)

@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    list_display = ('course', 'semester', 'year')
    search_fields = ('course', 'semester', 'year')

@admin.register(FeePayment)
class FeePaymentAdmin(admin.ModelAdmin):
    list_display = ('student', )
    search_fields = ('student', )

@admin.register(Admin)
class AddAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )

@admin.register(Faculty)
class facultyadmin(admin.ModelAdmin):
    list_display=('name','college_id','department','qualification','experience','date_of_joining','phone','gender','birthday','address','city','state','state_code')
    search_fields=('employee_id',)


from .models import ChatRoom,Message

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'participant1','participant2']
    

    
@admin.register(Message)
class Message_Student_faculty(admin.ModelAdmin):
    list_display=('chat_room','sender_id','content')
    search_fields=('chat_room','sender_id',)

@admin.register(Department)
class Department(admin.ModelAdmin):
    list_display=('name','code')
    search_fields=('name',)

@admin.register(Level)
class Level(admin.ModelAdmin):
    list_display=('name',)
    search_fields=('name',)

@admin.register(Position)
class Position(admin.ModelAdmin):
    list_display=('name','department','type')
    search_fields=('name',)


from .models import Students,History
@admin.register(Students)
class Students(admin.ModelAdmin):
    list_display=('name','roll_no','course')
    search_fields=('name',)


@admin.register(History)
class History(admin.ModelAdmin):
    list_display=('content','updatedFrom','updatedTo')
    search_fields=('content',)

@admin.register(Subject_Details)
class SubjectDetail(admin.ModelAdmin):
    list_display = ('serial_no', 'course','name','code', 'semester', 'level',)
    fields=('serial_no', 'course', 'name','code','semester', 'level','content')



from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'created_at']


from django.contrib import admin
from .models import FriendshipProposal

@admin.register(FriendshipProposal)
class FriendshipProposalAdmin(admin.ModelAdmin):
    list_display = ('id', 'decision', 'friend_name', 'user_phone', 'contact_choice', 'created_at', 'is_active')
    list_filter = ('decision', 'contact_choice', 'created_at', 'is_active')
    search_fields = ('friend_name', 'user_phone', 'user_email')
    readonly_fields = ('created_at', 'decision_made_at', 'contact_shared_at')
    list_per_page = 20
    
    fieldsets = (
        ('Proposal Information', {
            'fields': ('decision', 'decision_made_at', 'is_active')
        }),
        ('Contact Information', {
            'fields': ('friend_name', 'user_phone', 'user_email')
        }),
        ('Contact Decision', {
            'fields': ('contact_choice', 'contact_shared_at')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )

from django.contrib import admin
from .models import BirthdayGreeting

@admin.register(BirthdayGreeting)
class BirthdayGreetingAdmin(admin.ModelAdmin):
    # Display fields in admin list view
    list_display = ( 'photo', 'greeting_message', 'created_at')


    