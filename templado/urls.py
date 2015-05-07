from django.conf.urls import patterns, url
from .views import ReportsListView, TemplatesListView, ReportFormView, DownloadReport, EditReportFormView, \
    TemplateFormView, SearchView, HelpView, UploadStaticView

urlpatterns = patterns('',
    url(r'^uploadstatic/$', UploadStaticView.as_view(), name='upload-static'),
    url(r'^create/$', TemplateFormView.as_view(), name='template-form'),
    url(r'^search/$', SearchView.as_view(), name='search'),
    url(r'^edit/(?P<template>\d+)/$', TemplateFormView.as_view(), name='edit-template-form'),
    url(r'^generate/(?P<template>\d+)/$', ReportFormView.as_view(), name='report-form'),
    url(r'^regenerate/(?P<report>\d+)/$', EditReportFormView.as_view(), name='edit-report-form'),
    url(r'^reports$', ReportsListView.as_view(), name='report-list'),
    url(r'^download/(?P<report>\d+)/$', DownloadReport.as_view(), name='download-report'),
    url(r'^help$', HelpView.as_view(), name='help'),
    url(r'^$', TemplatesListView.as_view(), name='template-list'),
)