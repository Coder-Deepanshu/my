from django import forms
from .models import Student_add

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        label="",
        widget=forms.TextInput(attrs={'placeholder': 'Enter your Username'})
    )
    user_id = forms.CharField(
        max_length=100,
        label="",
        widget=forms.TextInput(attrs={'placeholder': 'Enter your User ID'})
    )

from django import forms
from .models import Student_add,result

class Addstudentform(forms.ModelForm):
    class Meta:
        model = Student_add
        exclude = ['Student_rollno','semester']  # <-- yahan sirf yeh line badli hai
        widgets = {
            'Student_name': forms.TextInput(attrs={'placeholder': 'Enter Full Name of the Student'}),
            'Father_name': forms.TextInput(attrs={'placeholder': 'Enter Father\'s Name'}),
            'phone_no': forms.TextInput(attrs={'placeholder': 'Enter Phone Number (e.g., 9876543210)'}),
            'Address': forms.TextInput(attrs={'placeholder': 'Enter Residential Address'}),
            'city': forms.TextInput(attrs={'placeholder': 'Enter your City Address'}),
            'state': forms.TextInput(attrs={'placeholder': 'Enter your State'}),
            'Email': forms.EmailInput(attrs={'placeholder': 'Enter Email Address (e.g., example@gmail.com)'}),
            'course': forms.Select(attrs={'placeholder': 'Select Course'}),
            'tenth_dmc': forms.TextInput(attrs={'placeholder': 'Enter Your 10th Percentage'}),
            'twelth': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
        }

class uploadresultform(forms.ModelForm):
    class Meta:
        model = result
        exclude = ['Student_rollno','course']  # <-- yahan sirf yeh line badli hai
        widgets = {
            'one': forms.TextInput(),
            'two': forms.TextInput(),
            'three': forms.TextInput(),
            'four': forms.TextInput(),
            'five': forms.TextInput(),
            'six': forms.TextInput(),
            'seven': forms.TextInput(attrs={'placeholder': 'Enter Email Address (e.g., example@gmail.com)'}),
            'eight': forms.TextInput(attrs={'placeholder': 'Select Course'}),
            'nine': forms.TextInput(attrs={'placeholder': 'Enter Your 10th Percentage'}),
            'ten': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'eleven': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'twelve': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'thirteen': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'fourteen': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'fifteen': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'sixteen': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'seventeen': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'eighteen': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'nineteen': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'twenty': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'twenty_one': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'twenty_two': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'twenty_three': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'twenty_four': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'twenty_five': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'twenty_six': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'twenty_seven': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'twenty_eight': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'twenty_nine': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'thirty': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'thirty_one': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'thirty_two': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'thirty_three': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'thirty_four': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'thirty_five': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'thirty_six': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'thirty_seven': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'thirty_eight': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'thirty_nine': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'fourty': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'fourty_one': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'fourty_two': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'fourty_three': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'fourty_five': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'fourty_six': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'fourty_seven': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'fourty_eight': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'fourty_nine': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'fifty': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'fifty_one': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'fifty_two': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'fifty_three': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'fifty_four': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'fifty_five': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'fifty_six': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'fifty_seven': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'fifty_eight': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'fifty_nine': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'sixty': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'sixty_one': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'sixty_two': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'sixty_three': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'sixty_four': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'})
                }

# for delete data
from django import forms

class DeleteStudentForm(forms.Form):
    roll_no = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Enter Roll Number'}),
        label="Roll Number")
    
#  for delete result
class delete_result(forms.Form):
    roll_no = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Enter Roll Number'}),
        label="Roll Number")

# for view the result
class view_result(forms.Form):
    roll_no = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Enter Roll Number'}),
        label="Roll Number")
    
from .models import Faculty
class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = '__all__'
        exclude = ('employee_id',)  # <-- sahi syntax
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter Full Name'}),
            'department': forms.TextInput(attrs={'placeholder': 'Enter Department'}),
            'qualification': forms.TextInput(attrs={'placeholder': 'Enter Qualification'}),
            'experience': forms.NumberInput(attrs={'placeholder': 'Enter Experience (e.g., 5.5)'}),
            'date_of_joining': forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter Phone Number'}),
            'gender': forms.Select(attrs={'placeholder': 'Select Gender'}),
            'dob': forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date'}),
            'address': forms.Textarea(attrs={'placeholder': 'Enter Address'}),
            'city': forms.TextInput(attrs={'placeholder': 'Enter City'}),
            'state': forms.TextInput(attrs={'placeholder': 'Enter State'}),
            'pin_code': forms.TextInput(attrs={'placeholder': 'Enter Pin Code'}),
        }





