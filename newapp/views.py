import csv
from django.http import HttpResponse
from django.shortcuts import render, redirect
from reportlab.pdfgen import canvas
from .form import LoginForm
from .models import Student_add, Student_percent
from newapp.models import result

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
        role=request.POST.get('role')
        if role =='admin':
            if (username == "Deepanshu" and password == "12345") or (username == "Zyasha" and password == "12346") :  # Replace with your logic
                # Set session data
                request.session['username1'] = username
                return redirect('dashboard')  # Redirect to the dashboard
            else:
                return redirect("login")
        elif role=='faculty':
            if username == 'Kunal' and password== "12345":
                request.session['username2']=username
                return redirect('dashboard1')
            else:
                return redirect("login")
        else :
            if username == 'Abhishek' and password== "12345":
                request.session['username3']=username
                return redirect('dashboard2')
            else:
                return redirect("login")

    return render(request, 'home.html')

def dashboard_view(request):
    # Check if the user is logged in
    username = request.session.get('username1')  # Retrieve username from session
    if username:
        return render(request, 'dashboard.html', {'username': username})
    else:
        return redirect('login') 

def dashboard1(request):
    # Check if the user is logged in
    username = request.session.get('username2')  # Retrieve username from session
    if username:
        return render(request, 'dashboard1.html', {'username': username})
    else:
        return redirect('login')  # Redirect to login if not logged in
    
def dashboard2(request):
    # Check if the user is logged in
    username = request.session.get('username3')  # Retrieve username from session
    if username:
        return render(request, 'dashboard2.html', {'username': username})
    else:
        return redirect('login') 

def logout_view(request):
    # Clear session data
    request.session.flush()
    return redirect('login')

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
                     # Result table me entry create karo
                result.objects.filter(Student_rollno=roll_no).delete()
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
            student = Student_add.objects.get(Student_rollno=roll_no)
            setattr(student, column, new_value)
            student.save()

            if column == "course":
                try:
                    student_result = result.objects.get(Student_rollno=student.Student_rollno)
                    student_result.course = new_value
                    student_result.save()
                except result.DoesNotExist:
                    pass

            return redirect('dashboard')
        except Student_add.DoesNotExist:
            error_message = "No student found with the provided roll number."

    return render(request, 'alter_student.html', {'error_message': error_message})


from .models import Student_add
from .form import Addstudentform
from django.db import models
def add_student(request):
    if request.method == 'POST':
        form = Addstudentform(request.POST)
        if form.is_valid():
            max_roll = Student_add.objects.aggregate(max_roll=models.Max('Student_rollno'))['max_roll']
            if max_roll is None:
                max_roll = 0
            else:
                try:
                    max_roll = int(max_roll)
                except ValueError:
                    max_roll = 0
            student = form.save(commit=False)
            student.Student_rollno = str(max_roll + 1)
            student.save()
            # Result entry create karo
            result.objects.get_or_create(
                Student_rollno=student.Student_rollno,
                defaults={'course': student.course}
            )
            return render(request, 'add_student.html', {
                'form': Addstudentform(),
                'success_message': 'Student added successfully!'
            })
        else:
            return render(request, 'add_student.html', {'form': form, 'error_message': form.errors})
    else:
        form = Addstudentform()
    return render(request, 'add_student.html', {'form': form})


from django.shortcuts import render, redirect
from .form import FacultyForm
from .models import Faculty

def add_faculty(request):
    if request.method == 'POST':
        form = FacultyForm(request.POST)
        if form.is_valid():
            max_id = Faculty.objects.aggregate(max_roll=models.Max('employee_id'))['max_roll']
            if max_id is None:
                max_id = 'GK20250'
            else:
                try:
                    max_id = str(max_id)
                except ValueError:
                    max_id = 'GK20250'
            faculty = form.save(commit=False)
            faculty.employee_id = max_id[0:6]+str(int(max_id[6])+1)
            faculty.save()
            return render(request, 'add_faculty.html', {
                'form': FacultyForm(),
                'success_message': '    Faculty added successfully!'
            })

        else:
            return render(request, 'add_faculty.html', {'form': form, 'error_message': form.errors})
    else:
        form = FacultyForm()
    return render(request, 'add_faculty.html', {'form':form})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Faculty  # or from your_app.models import Faculty


def delete_faculty(request):
    employee_id = request.GET.get('employee_id')
    if employee_id:
        faculty = get_object_or_404(Faculty, employee_id=employee_id)
        return render(request, 'delete_faculty.html', {'faculty': faculty})
    return render(request, 'delete_faculty.html')


def confirm_delete_faculty(request, faculty_id):
    faculty = get_object_or_404(Faculty, pk=faculty_id)
    if request.method == 'POST':
        faculty.delete()
        messages.success(request, f'Faculty {faculty.name} deleted successfully!')
        return redirect('delete_faculty')
    return redirect('delete_faculty')

def view_faculty(request):
    faculty = None
    error_message = None
    if request.method == 'GET':
        id= request.GET.get('employee_id')
        try:
            faculty = Faculty.objects.get(employee_id=id)
        except Faculty.DoesNotExist:
            error_message = "No Faculty found with the provided Employee ID."
    return render(request, 'view_faculty.html', {'faculty': faculty, 'error_message': error_message})