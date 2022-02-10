from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CurrentSession)
admin.site.register(CurrentTerm)
admin.site.register(SessionAndTerm)
admin.site.register(Subject)
admin.site.register(Class)
admin.site.register(Staff)
admin.site.register(Receipt)


@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
    pass

class FeeStructureInline(admin.TabularInline):
    model = FeeStructure

class ReceiptInline(admin.TabularInline):
    model = Receipt
@admin.register(Invoice)
class InvoiceInlineAdmin(admin.ModelAdmin):
    inlines = [
        FeeStructureInline,ReceiptInline
]

class StudentSubjectInline(admin.TabularInline):
    model = StudentSubject
@admin.register(CreateResult)
class CreateResultInlineAdmin(admin.ModelAdmin):
    inlines = [
        StudentSubjectInline
]