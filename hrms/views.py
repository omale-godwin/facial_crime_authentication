from django.db import models
from django.shortcuts import render,redirect, resolve_url,reverse, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from .models  import Employee, Department,Kin, Attendance, Leave, Recruitment
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, CreateView,View,DetailView,TemplateView,ListView,UpdateView,DeleteView
from .forms import RegistrationForm,LoginForm,EmployeeForm,KinForm,DepartmentForm,AttendanceForm, LeaveForm, RecruitmentForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.utils import timezone
import sys

import shutil
from PIL import Image
import numpy as np
from subprocess import PIPE, run
from deepface import DeepFace
import cv2
import numpy as np

video_capture = cv2.VideoCapture(0)
import os
from subprocess import PIPE, run
from django.db.models import Q


# Create your views here.
class Index(TemplateView):
   template_name = 'hrms/home/home.html'

#   Authentication
class Register (CreateView):
    model = get_user_model()
    form_class  = RegistrationForm
    template_name = 'hrms/registrations/register.html'
    success_url = reverse_lazy('hrms:login')
    
class Login_View(LoginView):
    model = get_user_model()
    form_class = LoginForm
    template_name = 'hrms/registrations/login.html'

    def get_success_url(self):
        url = resolve_url('hrms:dashboard')
        return url

class Logout_View(View):

    def get(self,request):
        logout(self.request)
        return redirect ('hrms:login',permanent=True)
    
    
 # Main Board   
class Dashboard(LoginRequiredMixin,ListView):
    template_name = 'hrms/dashboard/index.html'
    login_url = 'hrms:login'
    model = get_user_model()
    context_object_name = 'qset'            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['emp_total'] = Employee.objects.all().count()
        context['dept_total'] = Department.objects.all().count()
        context['admin_count'] = get_user_model().objects.all().count()
        context['workers'] = Employee.objects.order_by('-id')
        return context

# Employee's Controller
class Employee_New(LoginRequiredMixin,CreateView):
    model = Employee  
    form_class = EmployeeForm  
    template_name = 'hrms/employee/create.html'
    login_url = 'hrms:login'
    redirect_field_name = 'redirect:'
    
    
    
class Employee_All(LoginRequiredMixin,ListView):
    template_name = 'hrms/employee/index.html'
    model = Employee
    login_url = 'hrms:login'
    context_object_name = 'employees'
    paginate_by  = 5
    
class Employee_View(LoginRequiredMixin,DetailView):
    queryset = Employee.objects.all()
    template_name = 'hrms/employee/single.html'
    context_object_name = 'employee'
    login_url = 'hrms:login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            query = Kin.objects.get(employee=self.object.pk)
            context["kin"] = query
            return context
        except ObjectDoesNotExist:
            return context
        
class Employee_Update(LoginRequiredMixin,UpdateView):
    model = Employee
    template_name = 'hrms/employee/edit.html'
    form_class = EmployeeForm
    login_url = 'hrms:login'
    
    
class Employee_Delete(LoginRequiredMixin,DeleteView):
    pass

class Employee_Kin_Add (LoginRequiredMixin,CreateView):
    model = Kin
    form_class = KinForm
    template_name = 'hrms/employee/kin_add.html'
    login_url = 'hrms:login'
   

    def get_context_data(self):
        context = super().get_context_data()
        if 'id' in self.kwargs:
            emp = Employee.objects.get(pk=self.kwargs['id'])
            context['emp'] = emp
            return context
        else:
            return context

class Employee_Kin_Update(LoginRequiredMixin,UpdateView):
    model = Kin
    form_class = KinForm
    template_name = 'hrms/employee/kin_update.html'
    login_url = 'hrms:login'

    def get_initial(self):
        initial = super(Employee_Kin_Update,self).get_initial()
        
        if 'id' in self.kwargs:
            emp =  Employee.objects.get(pk=self.kwargs['id'])
            initial['employee'] = emp.pk
            
            return initial

#Department views

class Department_Detail(LoginRequiredMixin, ListView):
    context_object_name = 'employees'
    template_name = 'hrms/department/single.html'
    login_url = 'hrms:login'
    def get_queryset(self): 
        queryset = Employee.objects.filter(department=self.kwargs['pk'])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dept"] = Department.objects.get(pk=self.kwargs['pk']) 
        return context
    
class Department_New (LoginRequiredMixin,CreateView):
    model = Department
    template_name = 'hrms/department/create.html'
    form_class = DepartmentForm
    login_url = 'hrms:login'

class Department_Update(LoginRequiredMixin,UpdateView):
    model = Department
    template_name = 'hrms/department/edit.html'
    form_class = DepartmentForm
    login_url = 'hrms:login'
    success_url = reverse_lazy('hrms:dashboard')

#Attendance View

class Attendance_New (LoginRequiredMixin,CreateView):
    model = Attendance
    form_class = AttendanceForm
    login_url = 'hrms:login'
    template_name = 'hrms/attendance/create.html'
    success_url = reverse_lazy('hrms:attendance_new')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["today"] = timezone.localdate()
        pstaff = Attendance.objects.filter(Q(status='PRESENT') & Q (date=timezone.localdate())) 
        context['present_staffers'] = pstaff
        return context

class Attendance_Out(LoginRequiredMixin,View):
    login_url = 'hrms:login'

    def get(self, request,*args, **kwargs):

       user=Attendance.objects.get(Q(staff__id=self.kwargs['pk']) & Q(status='PRESENT')& Q(date=timezone.localdate()))
       user.last_out=timezone.localtime()
       user.save()
       return redirect('hrms:attendance_new')   

class LeaveNew (LoginRequiredMixin,CreateView, ListView):
    model = Leave
    template_name = 'hrms/leave/create.html'
    form_class = LeaveForm
    login_url = 'hrms:login'
    success_url = reverse_lazy('hrms:leave_new')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["leaves"] = Leave.objects.all()
        return context

class Payroll(LoginRequiredMixin, ListView):
    model = Employee
    template_name = 'hrms/payroll/index.html'
    login_url = 'hrms:login'
    context_object_name = 'stfpay'

class RecruitmentNew (CreateView):
    model = Recruitment
    template_name = 'hrms/recruitment/index.html'
    form_class = RecruitmentForm
    success_url = reverse_lazy('hrms:recruitment')

class RecruitmentAll(LoginRequiredMixin,ListView):
    model = Recruitment
    login_url = 'hrms:login'
    template_name = 'hrms/recruitment/all.html'
    context_object_name = 'recruit'

class RecruitmentDelete (LoginRequiredMixin,View):
    login_url = 'hrms:login'
    def get (self, request,pk):
     form_app = Recruitment.objects.get(pk=pk)
     form_app.delete()
     return redirect('hrms:recruitmentall', permanent=True)

class Pay(LoginRequiredMixin,ListView):
    model = Employee
    template_name = 'hrms/payroll/index.html'
    context_object_name = 'emps'
    login_url = 'hrms:login'

def capreg(request):
    run([sys.executable, '//home//omale//Desktop//deepface/faces.py'], shell=False)
    return render(request, 'hrms/staff/newcriminal.html')
def captures(request):

    models = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib"]
    # DeepFace.stream(os.getcwd() + '/media/photos/', enable_face_analysis=False)
    run([sys.executable, '//home//omale//Desktop//deepface/faces.py'], shell=False) 
    
    # DeepFace.stream(os.getcwd(), enable_face_analysis=False, source='http://192.168.43.1:8080/video' )
    for i in  os.listdir(r'/home/omale/Music/hr/hr2/HRMSPROJECT/media'):
        
        print(os.getcwd() + '/media/photos/' + i)
        results = DeepFace.verify( os.getcwd() + '/my_image.png', os.getcwd() + '/media/' + i, model_name = models[1], enforce_detection=False )
        if results['verified'] == True:
            request.session['users'] = i
            messages.success(request, 'successfully identify criminal')
            crimi = Employee.objects.get(thumb=i)
            print(os.getcwd() + '/my_image.png' + ' \n' + i)
            return redirect('hrms:employee_view', pk=crimi.id)
        print('iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')
        print(os.getcwd() + '/my_image.png' + ' \n' + i)
       
    messages.error(request, ' 𝔽𝕒𝕔𝕚𝕒𝕝 𝔸𝕦𝕥𝕙𝕖𝕟𝕥𝕚𝕔𝕒𝕥𝕚𝕠𝕟 𝔽𝕒𝕚𝕝')       
    return render(request, 'hrms/payroll/index.html')

def newcriminal(request):
    depa = Department.objects.all()
    for x in depa:
        list = [x.name]
    

    context = {
        'depa':list
    }
    print(list)
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        mobile = request.POST['mobile']
        email = request.POST['email']
        address = request.POST['address']
        emergency = request.POST['emergency']
        department = request.POST['department']
        joined = request.POST['joined']
        language = request.POST['language']
        nuban = request.POST['nuban']
        salary = request.POST['salary']
        bank = request.POST['bank']
        Crime_detail = request.POST['Crime_detail']
        occupation = request.POST['occupation']
        location = request.POST['location']
        gender = request.POST['gender']
        crime_date = request.POST['crime_date']
        crime_type = request.POST['crime_type']
        
        thumb  = first_name + '.png'
        os.rename('my_image.png', thumb)
        src_dir = os.getcwd() + '/' + thumb
        dst_dir = os.getcwd() + '/media'
        shutil.copy(src_dir, dst_dir )
        print(thumb)

        datas = Employee(first_name=first_name, last_name=last_name, mobile=mobile, email=email, address=address, thumb=thumb, emergency=emergency,
        department=department,joined=joined, gender=gender, language=language, nuban=nuban, salary=salary, bank=bank, occupation=occupation,
        location=location, Crime_detail=Crime_detail, crime_date=crime_date, crime_type=crime_type)
        if datas:
            print('ffffffffffffffffffffffffffffffffff')
        else:
            print('bbbbbbbbbbbbbbbbbbbbbbbb')
        datas.save()
    else:
        print('jjjjjjjjjjjjjjjjjjjjjjjj')  

    return render(request, 'hrms/staff/newcriminal.html', context)
        

    
