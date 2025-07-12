from django.contrib import admin
from .models import Student_add, Student_percent,result,subject

# Register the Student_add model
@admin.register(Student_add)
class StudentAddAdmin(admin.ModelAdmin):
    list_display = ('Student_name', 'Student_rollno', 'course')
    search_fields = ('Student_name', 'Student_rollno', 'course')

# Register the Student_percent model
@admin.register(Student_percent)
class StudentPercentAdmin(admin.ModelAdmin):
    list_display = ('Student_rollno', 'percentage')
    search_fields = ('Student_rollno',)

@admin.register(result)
class resultAdmin(admin.ModelAdmin):
    list_display = (
        'Student_rollno',  # Use correct field name
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










