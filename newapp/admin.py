from django.contrib import admin
from .models import Student,subject,Faculty,Course,Attendance,FeePayment,FeeStructure,Admin,StudentBalance
from .models import Department,Level,Position, StudentDocuments,AdminDocuments, FacultyDocuments
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


@admin.register(subject)
class subjectadmin(admin.ModelAdmin):
    list_display=('semester','course','I','II','III','IV','V','VI','VII','VIII')
    search_fields=('semester','course')

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






