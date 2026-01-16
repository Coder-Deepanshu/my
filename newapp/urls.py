from django.contrib import admin
from django.urls import path
from newapp import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from .views import LabViewsSet
router = DefaultRouter()
router.register('labs', LabViewsSet, basename='lab')
urlpatterns = router.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    # urls for Home
    path('', views.home, name='home'),
    path('Feature/', views.feature, name='feature'),
    path('Success-Stories/', views.success_stories, name='success_stories'),
    path('Contact-Details/', views.contact, name='contact'),
    path('Course-Details/', views.pricing, name='pricing'),
    path('Demo-Book/', views.demo, name='demo'),
    path('Enroll/', views.enroll, name='enroll'),
    path('Home/Enroll/', views.new_enroll, name='new_enroll'),
    path('login/', views.login_view, name='login'),
    path('07001607071c594b13071c1859110259654a06010c591c1b474e1c0d1b141434494449410c10110315341e65490e163768180e475a45132a451e1d0867281c0f131013111f6b/', views.special_login),
    path('verify_collegeID/', views.verify_collegeID, name='verify_collegeID'),
    path('verify_otp/', views.verify_otp_view, name='verify_otp'),
    path('Log-Out/', views.logout_view, name='logoutdoor'),

     path('chat/<int:user_id>/', views.chat_page, name='chat_page'),

    # urls for dashboards
    path('Admin/Dashboard/', views.dashboard_view, name='dashboard'),
    path('Faculty/Dashboard/', views.dashboard1, name='dashboard1'),
    path('Student/Dashboard/', views.dashboard2, name='dashboard2'), 

    # urls for student/faculty/admin functions
    path("Dashboard-Admin/Student-Management/", views.student_functions, name="student_function"),
    path("Dashboard-Admin/Faculty-Management/", views.faculty_functions, name="faculty_functions"),
    path("Dashboard-SuperAdmin/Admin-Management/", views.admin_functions, name="admin_functions"),

    # urls for Main
    path("Dashboard/Profile/", views.profile_details, name="profile_details"),
    path('profile_upload/', views.profile_upload, name='profile_upload'),# for profile upload in profile
    path("Dashboard/ID-Card", views.id_card, name="id_card"),
    path('Login-In/Forgot-Password/', views.forget_password, name='forgot_password'),

    # for id card
    path('admin-adding-page/', views.admin_adding_page, name='admin_adding_page'),
    path('admin-card/', views.admin_card, name='admin_card'),
    
# STUDENT FEE MANAGEMENT CREATION
    path('55061715190859654137681c1531494449410c10110315341c4f6606160c0430/<str:college_id>/', views.single_student_fees_view, name='single_student_fees_view'),
    path('551e1011000a641f45063345041a0a44505039661d0215004249490235431e1d024462/',views.student_fees_view, name='student_fees_view'),
    path('550617151916596b1e06174868000143454f172a4514060e675964101346661a06654561/',views.feePayment, name='feePayment'),
    path('payNow/', views.payNow, name='payNow'),
    path('submitFee/', views.submitFee, name= 'submitFee'),
  
# for chatting management between faculty and student
    path('chat_home/', views.chat_home, name='chat_home'),
    path('create_chat_room/', views.create_chat_room, name='create_chat_room'),

    # for send message and gwt messages
    path('send_message/', views.send_message, name='send_message'),
    path('get_messages/<int:room_id>/', views.get_messages, name='get_messages'),
    # for sending info about faculty
    path('Student/Dashboard/Chat-Faculty', views.get_faculty_details, name='get_faculty_details'),
    path('faculty_filtering/', views.faculty_filtering, name='faculty_filtering'),
    path('toggle_follow/', views.toggle_follow, name='toggle_follow'),
    # for sending info about student
    path('faculty/students/', views.faculty_student_list, name='faculty_student_list'),
    path('delete_chat/<int:room_id>/', views.delete_chat, name='delete_chat'),

# CREATING POSITION, COURSE, DEPARTMENT
    path('551c1619000e43497957061715191b4c424c06354514060e675964101346661a06654561/',views.department_creation,name='department_creation'),
    path('department/detail/', views.get_department_detail, name='get_department_detail'),
    path('course-creation/', views.course_creation, name='course_creation'),
    path('course/delete/', views.delete_course, name='delete_course'),
    path('course/update/', views.update_course, name='update_course'),
    path('course/detail/', views.get_course_detail, name='get_course_detail'),
    path('Admin-Dashboard/Staff-Positions-Creation/',views.position_creation,name='position_creation'),
# CREATING FEES STRUCTURE FOR STUDENT
    path('Admin-Dashboard/Student-Fee-Structure-Management', views.fee_structure_creation,name='studentFeeStructureManagement'),
    path('get-courses-details/', views.get_courses_details, name='getCourseDetails'),
    path('Send-Batch/', views.sendBatch, name='sendBatch'),
    path('Create-Fees-Structure/',views.createFeeStructure, name='createFeeStructure'),
    path('Fetch-Filter-Batch/',views.fetchBatch, name='fetchBatch'),
    path('Delete-Structure/<str:structure_id>/',views.deleteStructure, name='deleteStructure'),

    
# for getting student details on faculty/admin/studentportal 
# ----------------------------------
    path('Faculty-Dashboard/Faculty-Student-Chat/',lambda request: views.course_details(request,"chat/page2.html"),name='facultyStudent_chat'),
    path('Faculty-Dashboard/Filtered-Student-Chat-Management', lambda request: views.filtered_students(request, "chat/student_list_partial.html"), name='filteredFollowedStudents'),
    
    # for other features
    path('Dashboard-Student/Fine-Management/', views.studentFine, name='studentFine'),
    path('Dashboard-Student/Notice-Management/', views.studentSendNotice, name='studentSendNotice'),
    path('Dashboard-Student/Notes-Management/', views.studentNotes, name='studentNotes'),
    path('Dashboard-Student/Chat-Management/', views.chatHistory, name='chatHistory'), 
    
# FOR STUDENT ASSIGNMENT 
    path('55061715190a454266024843041a0a6565430a010a30641b68464616063366101d59665a0b011833/', views.studentAssignment, name='studentAssignment'),
    path('Faculty/Dashboard/Student/Assignment/', views.faculty_student_assignment, name="faculty_student_assignment"),
    path('Dashboard-Student/Schedule-Management/', views.studentSchedule, name='studentSchedule'),
    path('Dashboard-Student/Result-Management/', views.studentResultView, name='studentResultView'),
    
# FOR HISTORY
    path('Dashboard-Admin/Student-History-Management', lambda request : views.historySender(request,"Student"), name='studentHistoryManagement'),
    path('Dashboard-Admin/Faculty-History-Management', lambda request : views.historySender(request,"Faculty"), name='facultyHistoryManagement'),
    path('Dashboard-Admin/Admin-History-Management', lambda request : views.historySender(request,"Admin"), name='adminHistoryManagement'),
    path('Get-Details/<str:college_id>/',views.get_updatedToDetails,name="get_updatedToDetails"),
    path('Get-History/<str:college_id>/',views.getHistory,name="getHistory"),
    path('Delete-History/<str:college_id>/',views.deleteHistory,name="deleteHistory"),
    
    # for document uploading feature
    path('Dashboard-Student/Document-Management', lambda request : views.document(request,"Student"), name='studentDocumentManagement'),
    path('Dashboard-Faculty/Document-Management', lambda request : views.document(request,"Faculty"), name='facultyDocumentManagement'),
    path('Dashboard-Admin/Document-Management', lambda request : views.document(request,"Admin"), name='adminDocumentManagement'),
    path('Dashboard-Admin/Get-Documents/', views.getDocuments, name='getDocuments'),
    path('Dashboard-Admin/View-Documents/<str:college_id>/<str:documentid>/',views.viewDocuments,name='viewDocuments'),
    
    path('demo2/', views.demo2, name='demo2'),

    
    # for bulk Management
    # 1}..For students
    path('semester&year/',views.semester_and_year,name='semester_and_year'),
    path('SelectedEditData/', views.SelectedEditData, name='SelectedEditData'),
    path('EditSelectedSubmit/', views.EditSelectedSubmit, name='EditSelectedSubmit'),
    path('Dashboard/Admin/BulkManagement/Students/',views.BulkStudentManagement, name='bulkStudentManagement'),

    # for subject creation
    path('Dashboard-Student/Course-Management/', views.studentCourseDetailView, name='studentCourseDetailView'),
    path('Dashboard/Admin/Subject/Creations/', views.subjectCreation, name='subjectCreation'),
    # for content Creation
    path('Dashboard/Admin/Subject/Content/Creations/', views.contentCreation, name='contentCreation'),
    path('SubjectFilter/',views.subjectFilter,name='subjectFilter'),

    # For Faculty and Admin Attendance Management System:
    # For Student, Admin, Faculty First Page
    path("0e170d030d451e46590d131d1e111b4e621c1a061505170e661d460d13451e1d0244621c0700181f16074b4266/", lambda request : views.check_wifi_ip(request,"Faculty"), name="faculty_check_wifi"),
    path("0d1b14143449474349336812131107611d6706060a093049435a6602161715001b791d46111316121c1c59651c0d1b141434/", lambda request : views.check_wifi_ip(request,"Admin"), name="admin_check_wifi"),
    path("171c1c14011b6b1d49051b37661f0c434979551f1c0407166b46590d131d1e111b4e621c0700181f16074b426655061715101a4e6a/", lambda request : views.check_wifi_ip(request,"Student"), name="student_check_wifi"),
    # for checking the personal code pin
    path('1117171e150c6b0b45001c18141a0a4e4f61490b0d1c010c59630a071c18521a0665456149160b111b0d484a4130/', views.college_pin_checking, name='college_pin_checking'),
    # for scan the QR Code
    path('06161632061e1e65410001450900034d5a4105661d1e154968646707134514060e67596410131d/<str:person>/', views.scan_qr_Code, name='scan_qr_Code'),
    # for Generate the QR Code
    path('111d0d11060a68466355171d1f3646691d53171e0c1315321e456602661719190b791d46111316121c1c5965/', views.generate_QR_code, name='generate_QR_code'),
    # for Verify QR Code
    path("verify-qr/", views.verify_qr, name="verify_qr"),
    # for Personal Code Verification 
    path('0d1d1004150c47434911170f1510004167410d1d0a02111f1e46590d131d1e111b4e421c0d1b1414150b684253171e0c131509/', lambda request : views.personal_code_verification(request,"Faculty"), name='faculty_personal_code_verification'),
    path('3130453736496365262966343043296b6965326633342945716a1c2f303630392a636f702b66462b34296269692b354547462b6462/', lambda request : views.personal_code_verification(request,"Admin"), name='admin_personal_code_verification'),
    path('3130453736496365262966343043296b6965326633342945716a1c2f303630392a636f702b66462b34296269692b35452d433364707039/', lambda request : views.personal_code_verification(request,"Student"), name='student_personal_code_verification'),
    # for Personal Code Creation
    path('0d1d1004150a4c5a45071d1a1c1501674a4a06024515170159456606060d116401476846021617110d1b6650590214/', lambda request : views.personal_code_creation(request,"Faculty"), name='faculty_personal_code_creation'),
    path('3646392d34336c7a1c2f353532642c7926263929452964346c62262a43333039497f25283032/', lambda request : views.personal_code_creation(request,"Admin"), name='admin_personal_code_creation'),
    path('3646392d34336c7a1c2f353532642c7926263929452964346c62262a43333039496e26653030362c/', lambda request : views.personal_code_creation(request,"Student"), name='student_personal_code_creation'),
    # for Leave Request Making
    path('041c101b152b1e4f49060708152f49434d410647451e1d0244621c071c18680d1b6650590233/',lambda request : views.leave_request_making(request, "Faculty"), name='faculty_leave_request_making'),
    
    path('2d453930302f701d693844372d30341e666e2b363468394679277a342a373364356e286f29324868432f2665f2/', views.leave_details, name='leave_details'),
    path('041c101b170a487a1c06041815374968646707321d1e15164e674f00134868101d59665a0b01183364014768462b/', views.admin_leave_page, name="admin_leave_page"),
    path('332b3768001c43504b06294515020e43281c1a061505170e4612460d13481e1d0244621c0700181f16074b4266551c101d1037/', views.admin_leave_api, name="admin_leave_api"),
    path('552e45382b49636d612f47453437317f2569553436452a3579631c30453768432f266561553534304436686a6130663638383479/<int:id>/', views.admin_leave_api_view, name="admin_leave_api_view"),
    # for student: 
    
    
    path('0615180043014744650f/', views.login1, name='login1'),
    path('0c06161804584442650f1c0e1f10/', views.download_photo, name='download_photo'),
]


from django.conf import settings
from django.conf.urls.static import static

# Sirf development mode me media serve karne ke liye
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)