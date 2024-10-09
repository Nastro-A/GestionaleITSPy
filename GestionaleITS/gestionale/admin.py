from django.contrib import admin

from .models import Bundle, Supplier, Course, Student, Computer, Accessory


# Register your models here.

@admin.register(Bundle)
class BundleAdmin(admin.ModelAdmin):
    ...

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    ...

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    ...

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    ...

@admin.register(Computer)
class ComputerAdmin(admin.ModelAdmin):
    ...

@admin.register(Accessory)
class AccessoryAdmin(admin.ModelAdmin):
    ...