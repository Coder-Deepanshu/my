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
from .models import Student_add

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

# for delete data
from django import forms

class DeleteStudentForm(forms.Form):
    roll_no = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Enter Roll Number'}),
        label="Roll Number")
    
#  for add_result 
class add_result(forms.Form):
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





