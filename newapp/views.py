import csv
from django.http import HttpResponse
from django.shortcuts import render, redirect
from reportlab.pdfgen import canvas
from .form import LoginForm
from .models import Student_add, Student_percent

def generate_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'

    # Create a CSV writer object.
    writer = csv.writer(response)

    # Write the header row.
    writer.writerow(['Column 1', 'Column 2', 'Column 3'])

    # Write some example data rows.
    writer.writerow(['Row 1 Col 1', 'Row 1 Col 2', 'Row 1 Col 3'])
    writer.writerow(['Row 2 Col 1', 'Row 2 Col 2', 'Row 2 Col 3'])

    return response

def generate_pdf(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="students.pdf"'

    # Create a PDF object using ReportLab.
    p = canvas.Canvas(response)

    # Write content to the PDF.
    students = Student_add.objects.all()
    y = 800  # Start position for writing
    p.drawString(100, y, "Student List")
    y -= 20
    for student in students:
        p.drawString(100, y, f"Roll No: {student.Student_rollno}, Name: {student.Student_name}, Class: {student.course}")
        y -= 20

    # Finalize the PDF.
    p.showPage()
    p.save()

    return response

def login_view(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        # form = LoginForm(request.POST)
    
            # username = form.cleaned_data['username']
            # user_id = form.cleaned_data['user_id']

            # Custom authentication logic
        if (username == "Deepanshu" and password == "12345") or (username == "Zyasha" and password == "12346") :  # Replace with your logic
                # Set session data
                request.session['username'] = username
                return redirect('dashboard')  # Redirect to the dashboard
        else:
                return redirect("invalid")
    # else:
    #     form = LoginForm()
    return render(request, 'home.html')

def dashboard_view(request):
    # Check if the user is logged in
    username = request.session.get('username')  # Retrieve username from session
    if username:
        return render(request, 'dashboard.html', {'username': username})
    else:
        return redirect('login')  # Redirect to login if not logged in

def logout_view(request):
    # Clear session data
    request.session.flush()
    return redirect('login')
# for valid page
def valid(request):
    return render(request,'success.html')
# for invalid form
def invalid(request):
    return render(request,'invalid.html')
def DelValid(request):
    return render(request,'deletestudentvalid.html')

from .models import Student_add
from .form import DeleteStudentForm

def delete_student_view(request):
    if request.method == 'POST':
        form = DeleteStudentForm(request.POST)
        if form.is_valid():
            roll_no = form.cleaned_data['roll_no']

            # Check if the student exists in the database
            try:
                student = Student_add.objects.get(Student_rollno=roll_no)
                student.delete()  # Delete the student
                return render(request,'delete_student.html',{'success_message':f'Student with Roll no.{roll_no} has been successfully deleted!'})  # Redirect to a success page
            except Student_add.DoesNotExist:
                return render(request, 'delete_student.html', {'error_message': f'Student  with Roll No {roll_no} does not exist.'})
    else:
        form = DeleteStudentForm()
    return render(request, 'delete_student.html', {'form': form})

from django.shortcuts import render
from .models import Student_add
# for viewing the student details
def view_student(request):
    student = None
    error_message = None
    if request.method == 'POST':
        roll_no = request.POST.get('roll_no')
        try:
            student = Student_add.objects.get(Student_rollno=roll_no)
        except Student_add.DoesNotExist:
            error_message = "No student found with the provided roll number."
    return render(request, 'view_student.html', {'student': student, 'error_message': error_message})


#  for altering student
def alter_student(request):
    error_message = None
    if request.method == 'POST':
        roll_no = request.POST.get('roll_no')
        column = request.POST.get('column')
        new_value = request.POST.get('new_value')

        try:
            # Fetch the student record
            student = Student_add.objects.get(Student_rollno=roll_no)
            
            # Dynamically update the selected column
            setattr(student, column, new_value)
            student.save()  # Save the changes to the database
            
            return redirect('dashboard')  # Redirect to dashboard after successful update
        except Student_add.DoesNotExist:
            error_message = "No student found with the provided roll number."

    return render(request, 'alter_student.html', {'error_message': error_message})

# to generate id card
from django.shortcuts import render
from .models import Student_add

from django.shortcuts import render, redirect
from .form import Addstudentform
from .models import Student_add
from django.db import models

def add_student(request):
    if request.method == 'POST':
        form = Addstudentform(request.POST, request.FILES)
        if form.is_valid():
            max_roll = Student_add.objects.aggregate(max_roll=models.Max('Student_rollno'))['max_roll']
            if max_roll is None:
                max_roll = 0
            else:
                max_roll = int(max_roll)  # <-- yahan typecast kiya
            student = form.save(commit=False)
            student.Student_rollno = max_roll + 1
            student.save()
            return render(request, 'add_student.html', {'success_message': 'Student added successfully!'})
        else:
            return render(request, 'add_student.html', {'form': form, 'error_message': form.errors})
    else:
        form = Addstudentform()
    return render(request, 'add_student.html', {'form': form})
# from .models import user1

# user1.objects.create(name="Deepanshu",age=25)




