from django.contrib import admin
from django.urls import path
from newapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logoutdoor'),
    path('valid/',views.valid,name='valid'),
    path('invalid/',views.invalid,name='invalid'),
    path('delete-student/', views.delete_student_view, name='delete_student'),
    path('generate-pdf/', views.generate_pdf, name='generate_pdf'),
    path('generate-csv/', views.generate_csv, name='generate_csv'),
    path('view-student/', views.view_student, name='view_student'),
    path('delval/',views.DelValid,name="delvalid"),
    path('add_student/',views.add_student,name='add_student'),
    path('alter_student/',views.alter_student,name='alter_student')


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)