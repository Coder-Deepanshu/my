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
                     # Result table me entry create karo
                from .models import result
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

# to generate id card
from django.shortcuts import render
from .models import Student_add

from django.shortcuts import render, redirect
from .form import Addstudentform
from .models import Student_add,result,subject
from django.db import models

def add_student(request):
    if request.method == 'POST':
        form = Addstudentform(request.POST, request.FILES)
        if form.is_valid():
            max_roll = Student_add.objects.aggregate(max_roll=models.Max('Student_rollno'))['max_roll']
            if max_roll is None:
                max_roll = 0
            else:
                max_roll = int(max_roll)
            student = form.save(commit=False)
            student.Student_rollno = max_roll + 1
            student.save()
            
            # Result table me entry create karo (Student_rollno string pass karo)
            from .models import result
            result.objects.create(
                Student_rollno=str(student.Student_rollno),
                course=student.course
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

def check_rollno(request):
    if request.method == 'POST':
        rollno = request.POST.get('roll_no')
        try:
            student_detail = Student_add.objects.get(Student_rollno=rollno)
            sem = student_detail.semester
            course = student_detail.course
            name = student_detail.Student_name

            result_obj = result.objects.get(Student_rollno=rollno)

            if sem == 'I':
                subject_detail = subject.objects.get(course=course, semester=sem)
                subjects = [
                    subject_detail.I, subject_detail.II, subject_detail.III, subject_detail.IV,
                    subject_detail.V, subject_detail.VI, subject_detail.VII, subject_detail.VIII
                ]
                return render(request, 'upload_result.html', {
                    'rollno': rollno,
                    'name': name,
                    'course': course,
                    'semester': sem,
                    'subjects': subjects
                })
            else:
                return render(request, 'add_result.html', {'error_message': 'Semester not supported.'})
        except (Student_add.DoesNotExist, result.DoesNotExist, subject.DoesNotExist):
            return render(request, 'add_result.html', {'error_message': 'Roll number not found or subject not found.'})
    else:
        return render(request, 'add_result.html')

def upload_result(request):
    if request.method == 'POST':
        rollno = request.POST.get('roll_no')
        marks = [request.POST.get(f'marks{i}') for i in range(1, 9)]
        try:
            # Get result entry for this rollno
            result_obj = result.objects.get(Student_rollno=rollno)
            result_obj.one = marks[0]
            result_obj.two = marks[1]
            result_obj.three = marks[2]
            result_obj.four = marks[3]
            result_obj.five = marks[4]
            result_obj.six = marks[5]
            result_obj.seven = marks[6]
            result_obj.eight = marks[7]
            result_obj.save()
            return render(request, 'add_result.html', {'success_message': 'Marks uploaded successfully!'})
        except result.DoesNotExist:
            # Agar result entry nahi mili, dobara marks input form dikhao
            try:
                student_detail = Student_add.objects.get(Student_rollno=rollno)
                sem = student_detail.semester
                course = student_detail.course
                name = student_detail.Student_name
                if sem == 'I':
                    subject_detail = subject.objects.get(course=course, semester=sem)
                    subjects = [
                        subject_detail.I, subject_detail.II, subject_detail.III, subject_detail.IV,
                        subject_detail.V, subject_detail.VI, subject_detail.VII, subject_detail.VIII
                    ]
                    return render(request, 'upload_result.html', {
                        'rollno': rollno,
                        'name': name,
                        'course': course,
                        'semester': sem,
                        'subjects': subjects,
                        'error_message': 'Result entry not found. Please check roll number.'
                    })
                else:
                    return render(request, 'add_result.html', {'error_message': 'Semester not supported.'})
            except (Student_add.DoesNotExist, subject.DoesNotExist):
                return render(request, 'add_result.html', {'error_message': 'Roll number or subject not found.'})
    else:
        return redirect('add_result')
