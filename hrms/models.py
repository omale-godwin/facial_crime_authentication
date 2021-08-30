from django.db import models
import random
from django.urls import reverse
from django.utils import timezone
import time
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    thumb = models.ImageField()

# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=70, null=False, blank=False)
    history = models.TextField(max_length=1000,null=True,blank=True, default='No History')
    

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("hrms:dept_detail", kwargs={"pk": self.pk})
    

class Employee(models.Model):
    lan = models.CharField(max_length=200, blank=True, null=True)
    gen = models.CharField(max_length=200, blank=True, null=True)
    emp_id = models.CharField(max_length=70, default='crm'+str(random.randrange(100,999,1)))
    thumb = models.ImageField(blank=True,null=True)
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    mobile = models.CharField(max_length=15)
    email = models.EmailField(max_length=125, null=False)
    address = models.TextField(max_length=100, default='')
    emergency = models.CharField(max_length=11)
    gender = models.CharField(blank=True, null=True, default='male', max_length=10)
    department = models.CharField(max_length=200,  blank=True, null=True)
    joined = models.CharField(max_length=200, blank=True, null=True)
    language = models.CharField( blank=True, null=True, max_length=10, default='english')
    nuban = models.CharField(max_length=10, default='0123456789')
    bank = models.CharField(max_length=25, default='First Bank Plc')
    salary = models.CharField(max_length=16,default='00,000.00')  
    crime_date = models.CharField(max_length=200, null=True, blank=True)
    crime_type = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    Crime_detail = models.CharField(max_length=200, blank=True, null=True)
    occupation = models.CharField(max_length=200, blank=True, null=True)    
    def __str__(self):
        return self.first_name
        
    def get_absolute_url(self):
        return reverse("hrms:employee_view", kwargs={"pk": self.pk})
    

class Kin(models.Model):
    crime_date = models.CharField(max_length=20, blank=True, null=True)
    crime_type = models.CharField(max_length=20, blank=True, null=True)
    Crime_detail = models.TextField(max_length=100, blank=True, null=True)
    occupation = models.CharField(max_length=20, blank=True, null=True)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    employee = models.OneToOneField(Employee,on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return self.first_name+'-'+self.last_name
    
    def get_absolute_url(self):
        return reverse("hrms:employee_view",kwargs={'pk':self.employee.pk})
    

class Attendance (models.Model):
    STATUS = (('PRESENT', 'PRESENT'), ('ABSENT', 'ABSENT'),('UNAVAILABLE', 'UNAVAILABLE'))
    date = models.DateField(auto_now_add=True)
    first_in = models.TimeField()
    last_out = models.TimeField(null=True)
    status = models.CharField(choices=STATUS, max_length=15 )
    staff = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)

    def save(self,*args, **kwargs):
        self.first_in = timezone.localtime()
        super(Attendance,self).save(*args, **kwargs)
    
    def __str__(self):
        return 'Attendance -> '+str(self.date) + ' -> ' + str(self.staff)

class Leave (models.Model):
    STATUS = (('approved','APPROVED'),('unapproved','UNAPPROVED'),('decline','DECLINED'))
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    start = models.CharField(blank=False, max_length=15)
    end = models.CharField(blank=False, max_length=15)
    status = models.CharField(choices=STATUS,  default='Not Approved',max_length=15)

    def __str__(self):
        return self.employee + ' ' + self.start

class Recruitment(models.Model):
    first_name = models.CharField(max_length=25)
    last_name= models.CharField(max_length=25)
    position = models.CharField(max_length=15)
    email = models.EmailField(max_length=25)
    phone = models.CharField(max_length=11)

    def __str__(self):
        return self.first_name +' - '+self.position
