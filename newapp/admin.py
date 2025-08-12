from django.contrib import admin
from .models import Student,result,subject,Faculty,Course,Attendance,FeePayment,FeeStructure,Admin,StudentBalance

@admin.register(StudentBalance)
class StudentAddAdmin(admin.ModelAdmin):
    list_display = ('student', 'extra_amount')
    search_fields = ('student',)

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



# Register the Student_percent model
@admin.register(result)
class resultAdmin(admin.ModelAdmin):
    list_display = (
        'Student_rollno','course',  # Use correct field name
        # Remove 'course' from list_display
        'one','two','three','four','five','six','seven','eight','nine','ten',
        'eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen',
        'nineteen','twenty','twenty_one','twenty_two','twenty_three','twenty_four',
        'twenty_five','twenty_six','twenty_seven','twenty_eight','twenty_nine',
        'thirty','thirty_one','thirty_two','thirty_three','thirty_four','thirty_five',
        'thirty_six','thirty_seven','thirty_eight','thirty_nine','fourty','fourty_one',
        'fourty_two','fourty_three','fourty_four','fourty_five','fourty_six','fourty_seven',
        'fourty_eight','fourty_nine','fifty','fifty_one','fifty_two','fifty_three','fifty_four',
        'fifty_five','fifty_six','fifty_seven','fifty_eight','fifty_nine','sixty','sixty_one',
        'sixty_two','sixty_three','sixty_four'
    )
    search_fields = ('Student_rollno',)

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
    list_display = ['name', 'display_participants']
    
    def display_participants(self, obj):
        return ", ".join([user.username for user in obj.participants.all()])
    display_participants.short_description = 'Participants'

    
@admin.register(Message)
class Message_Student_faculty(admin.ModelAdmin):
    list_display=('chat_room','sender','content')
    search_fields=('chat_room','sender',)













