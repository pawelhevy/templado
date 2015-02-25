from django.contrib import admin

# Register your models here.
from models import ReportTemplate, Report

admin.site.register(ReportTemplate)
admin.site.register(Report)