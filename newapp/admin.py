from django.contrib import admin
from .models import Student,result,subject,Faculty_Add,Course

# Register the Student_add model
@admin.register(Student)
class StudentAddAdmin(admin.ModelAdmin):
    list_display = ('name', 'roll_no', 'course')
    search_fields = ('name', 'roll_no', 'course')

@admin.register(Course)
class coursesAdmin(admin.ModelAdmin):
    list_display=('name','no_of_years','no_of_semesters')
    search_fields=('name',)

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

@admin.register(Faculty_Add)
class facultyadmin(admin.ModelAdmin):
    list_display=('name','employee_id','department','qualification','experience','date_of_joining','phone','gender','dob','address','city','state','pin_code')
    search_fields=('employee_id',)












