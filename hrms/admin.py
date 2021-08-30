from django.contrib import admin
from .models import Employee,Department,Attendance,Kin
# Register your models here.

class Criminal(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'thumb')
    list_display_links = ('id', 'first_name')
    list_per_page = 25
admin.site.register(Employee, Criminal)


admin.site.register([Department,Attendance,Kin])
