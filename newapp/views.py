import csv
from django.http import HttpResponse
from django.shortcuts import render, redirect
from reportlab.pdfgen import canvas
from .form import LoginForm
from .models import Student_add, Student_percent, BBA, BCA, B_Sc, B_Com, B_A

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

# for BBA
from .form import B_B_A , B_C_A , B_a , B_com , B_sc

def Bba(request):
    if request.method == 'POST':
        form = B_B_A(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Result Uploaded Successfully")
        else:
            return render(request, 'BBA.html', {'form': form, 'error_message': form.errors})
    else:
        form = B_B_A()
    return render(request, 'BBA.html', {'form': form})

# for BCA
def Bca(request):
    if request.method =='POST':
        form = B_C_A(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Result Uploaded Successfully")
        else:
            return HttpResponse(f"Error{form.errors}")
    else:
        form=B_C_A()
    return render(request,'BCA.html',{'form':form})

# for b.com
def Bcom(request):
    if request.method =='POST':
        form = B_com(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Result Uploaded Successfully")
        else:
            return HttpResponse(f"Error{form.errors}")
    else:
        form=B_com()
    return render(request,'B_Com.html',{'form':form})

# for b.a
def Ba(request):
    if request.method =='POST':
        form = B_a(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Result Uploaded Successfully")
        else:
            return HttpResponse(f"Error{form.errors}")
    else:
        form=B_a()
    return render(request,'BA.html',{'form':form})

# for b.sc
def Bsc(request):
    if request.method =='POST':
        form = B_sc(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Result Uploaded Successfully")
        else:
            return HttpResponse(f"Error{form.errors}")
    else:
        form=B_sc()
    return render(request,'B_Sc.html',{'form':form})

# for add result:
from .form import add_result
def add_results(request):
    if request.method == 'POST':
        form = add_result(request.POST)
        if form.is_valid():
            roll_no = form.cleaned_data['roll_no']
            try:
                student = Student_add.objects.get(Student_rollno=roll_no)
                course = student.course
                if course == 'B.B.A':
                    return redirect('BBA')
                elif course == 'B.C.A':
                    return redirect('BCA')
                elif course == 'B.Sc':
                    return redirect('B_Sc')
                elif course == 'B.Com':
                    return redirect('B_Com')
                elif course == 'B.A':
                    return redirect('BA')
                else:
                    return render(request, 'invalid.html', {'error_message': 'Invalid course.'})
            except Student_add.DoesNotExist:
                return render(request, 'invalid.html', {'error_message': 'Student does not exist.'})
    else:
        form = add_result()
    return render(request, 'add_result.html', {'form': form})


from django.contrib import messages
# for delete result
from .models import BBA,BCA,B_Com,B_Sc,B_A
from .form import delete_result
def Delete_result(request):
    if request.method=='POST':
        form=delete_result(request.POST)
        if form.is_valid():
            roll_no=form.cleaned_data['roll_no']
            try:
                student=Student_add.objects.get(Student_rollno=roll_no)
                course=student.course
                namE=student.Student_name
                if course=='B.B.A':
                    Name=BBA.objects.get(name=namE)
                    Name.delete()
                    messages.success(request, f"Result for roll number {roll_no} deleted successfully!")
                elif course == 'B.C.A':
                   Name=BCA.objects.get(name=namE)
                   Name.delete()
                   messages.success(request, f"Result for roll number {roll_no} deleted successfully!")
                elif course == 'B.Sc':
                    Name=B_Sc.objects.get(name=namE)
                    Name.delete()
                    messages.success(request, f"Result for roll number {roll_no} deleted successfully!")
                elif course == 'B.Com':
                    Name=B_Com.objects.get(name=namE)
                    Name.delete()
                    messages.success(request, f"Result for roll number {roll_no} deleted successfully!")
                elif course == 'B.A':
                    Name=B_A.objects.get(name=namE)
                    Name.delete()
                    messages.success(request, f"Result for roll number {roll_no} deleted successfully!")
                else:
                    messages.error(request, f"Roll number {roll_no} does not exist!")
            except Student_add.DoesNotExist:
               messages.error(request, f"Roll number {roll_no} does not exist!")
    else:
        form = add_result()
    return render(request, 'delete_result.html')

# for viewing student result
from .form import view_result
def View_result(request):
    bba=None
    bca=None
    bcom=None
    bsc=None
    ba=None
    error_message=None
    if request.method=='POST':
        form=view_result(request.POST)
        if form.is_valid():
            roll_no=form.cleaned_data['roll_no']
            try:
                student=Student_add.objects.get(Student_rollno=roll_no)
                course=student.course
                namE=student.Student_name
                if course=='B.B.A':
                    bba=BBA.objects.get(name=namE)
                    redirect('view2')
                elif course == 'B.C.A':
                   bca=BCA.objects.get(name=namE)
                   redirect('view2')
                elif course == 'B.Sc':
                    bsc=B_Sc.objects.get(name=namE)
                    redirect('view2')
                elif course == 'B.Com':
                    bcom=B_Com.objects.get(name=namE)
                    redirect('view2')
                elif course == 'B.A':
                    ba=B_A.objects.get(name=namE)
                    redirect('view2')
            except Student_add.DoesNotExist:
              error_message = "No student found with the provided roll number."
    else:
        form = view_result()
    return render(request, 'view_result2.html', {'form':form,'bba': bba , 'error_message':error_message,'bca':bca,'ba':ba,'bcom':bcom,'bsc':bsc})

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

def generate_id_card(request):
    error_message = None
    student = None

    if request.method == 'POST':
        roll_no = request.POST.get('roll_no')

        try:
            # Fetch the student record
            student = Student_add.objects.get(Student_rollno=roll_no)
        except Student_add.DoesNotExist:
            error_message = "No student found with the provided roll number."

    return render(request, 'id_card.html', {'student': student, 'error_message': error_message})


# for generate degree
def generate_degree(request):
    degree_error_message = None
    student = None
    percentage = None  # To store the calculated percentage

    if request.method == 'POST':
        roll_no = request.POST.get('roll_no')

        try:
            # Fetch the student record
            student = Student_add.objects.get(Student_rollno=roll_no)
            course = student.course
            namE = student.Student_name

            # Calculate percentage based on course
            if course == 'B.B.A':
                bba = BBA.objects.get(name=namE)
                total_marks = (
                    int(bba.management) +
                    int(bba.economics) +
                    int(bba.mathematics) +
                    int(bba.accounting) +
                    int(bba.communication) +
                    int(bba.computer)
                )
                percentage = round((total_marks / 600) * 100, 2)

            elif course == 'B.C.A':
                bca = BCA.objects.get(name=namE)
                total_marks = (
                    int(bca.C) +
                    int(bca.Digital_Electronics) +
                    int(bca.mathematics_I) +
                    int(bca.communication) +
                    int(bca.computer)
                )
                percentage = round((total_marks / 500) * 100, 2)

            elif course == 'B.Sc':
                bsc = B_Sc.objects.get(name=namE)
                total_marks = (
                    int(bsc.Physics) +
                    int(bsc.Chemistry) +
                    int(bsc.mathematics_I) +
                    int(bsc.communication) +
                    int(bsc.Environmental_science) +
                    int(bsc.computer)
                )
                percentage = round((total_marks / 600) * 100, 2)

            elif course == 'B.Com':
                bcom = B_Com.objects.get(name=namE)
                total_marks = (
                    int(bcom.Financial_Accounting) +
                    int(bcom.Business_management) +
                    int(bcom.mathematics) +
                    int(bcom.communication) +
                    int(bcom.environmental_studies)
                )
                percentage = round((total_marks / 500) * 100, 2)

            elif course == 'B.A':
                ba = B_A.objects.get(name=namE)
                total_marks = (
                    int(ba.history) +
                    int(ba.political_science) +
                    int(ba.sociology) +
                    int(ba.psychology) +
                    int(ba.economics) +
                    int(ba.english_literature) +
                    int(ba.hindi)
                )
                percentage = round((total_marks / 700) * 100, 2)

            # Save the percentage in the Student_percent table
            Student_percent.objects.update_or_create(
                Student_rollno=roll_no,
                defaults={'percentage': percentage}
            )

        except Student_add.DoesNotExist:
            degree_error_message = "No student found with the provided roll number."
        except Exception as e:
            degree_error_message = f"An error occurred: {str(e)}"

    # Retrieve the saved percentage for the student
    student_percent = None
    if percentage is not None:
        try:
            student_percent = Student_percent.objects.get(Student_rollno=roll_no)
        except Student_percent.DoesNotExist:
            degree_error_message = "Percentage not found for the student."

    return render(request, 'degree.html', {
        'student': student,
        'student_percent': student_percent,
        'degree_error_message': degree_error_message
    })


from django.shortcuts import render, redirect
from .form import Addstudentform
from .models import Student_add,result
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




