from django.contrib import admin
from .models import Student_add, Student_percent, BBA, BCA, B_Sc, B_Com, B_A,result

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

# Register the BBA model
@admin.register(BBA)
class BBAAdmin(admin.ModelAdmin):
    list_display = ('name', 'management', 'economics', 'mathematics', 'accounting', 'communication', 'computer')
    search_fields = ('name',)

# Register the BCA model
@admin.register(BCA)
class BCAAdmin(admin.ModelAdmin):
    list_display = ('name', 'C', 'Digital_Electronics', 'mathematics_I', 'communication', 'computer')
    search_fields = ('name',)

# Register the B_Sc model
@admin.register(B_Sc)
class BScAdmin(admin.ModelAdmin):
    list_display = ('name', 'Physics', 'Chemistry', 'mathematics_I', 'communication', 'Environmental_science', 'computer')
    search_fields = ('name',)

# Register the B_Com model
@admin.register(B_Com)
class BComAdmin(admin.ModelAdmin):
    list_display = ('name', 'Financial_Accounting', 'Business_management', 'mathematics', 'communication', 'environmental_studies')
    search_fields = ('name',)

# Register the B_A model
@admin.register(B_A)
class BAAdmin(admin.ModelAdmin):
    list_display = ('name', 'history', 'political_science', 'sociology', 'psychology', 'economics', 'english_literature', 'hindi')
    search_fields = ('name',)

@admin.register(result)
class resultAdmin(admin.ModelAdmin):
    list_display=('roll_no','course','one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','nineteen','twenty','twenty_one','twenty_two','twenty_three','twenty_four','twenty_five','twenty_six','twenty_seven','twenty_eight','twenty_nine','thirty','thirty_one','thirty_two','thirty_three','thirty_four','thirty_five','thirty_six','thirty_seven','thirty_eight','thirty_nine','fourty','fourty_one','fourty_two','fourty_three','fourty_four','fourty_five','fourty_six','fourty_seven','fourty_eight','fourty_nine','fifty','fifty_one','fifty_two','fifty_three','fifty_four','fifty_five','fifty_six','fifty_seven','fifty_eight','fifty_nine','sixty','sixty_one','sixty_two','sixty_three','sixty_four')
    search_fields=('roll_no','course',)








