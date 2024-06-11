"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, Recruiting_site='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), Recruiting_site='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from backend.gui.views.views import SampleTrackingView, FilteredSamplesView, AllSamplesView, some_streaming_csv_view,\
    UploadView, DashBoardView, LoginView, SearchView, log_out, csv_template_download, FilteredDownloadView, ContactView, ImprintView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", SampleTrackingView.as_view(), name="config"),
    path("samples/", AllSamplesView.as_view(), name="all_samples"),
    path("samples/filtered", FilteredSamplesView.as_view(), name="filtered_samples"),
    path("csv/", some_streaming_csv_view, name="csv"),
    path("filtered_download/", FilteredDownloadView.as_view(), name="filtered_download"),
    path("csv_template/", csv_template_download, name="csv_template"),
    path("upload/", UploadView.as_view(), name="upload"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("imprint/", ImprintView.as_view(), name="imprint"),
    path("dashboard/", DashBoardView.as_view(), name="dashboard"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", log_out, name="logout"),
    path("search/", SearchView.as_view(), name="search"),

    path("password_change/",
         auth_views.PasswordChangeView.as_view(
             template_name="gui/password_handling/password_change.html",
             success_url="./done/"),
         name="password_change"),

    path("password_change/done/",
         auth_views.PasswordChangeDoneView.as_view(
             template_name="gui/password_handling/password_change_done.html"),
         name="password_change_done"),

    path("password_reset/",
         auth_views.PasswordResetView.as_view(
             template_name="gui/password_handling/password_reset.html",
             extra_context={'user': None},
             email_template_name="gui/password_handling/password_reset_email.html",
             subject_template_name="gui/password_handling/password_reset_email_subject.txt",
             from_email="saturn3@uniklinik-freiburg.de"),
         name="password_reset"),

    path("password_reset/done",
         auth_views.PasswordResetDoneView.as_view(
             template_name="gui/password_handling/password_reset_done.html",
             extra_context={'user': None}),
         name="password_reset_done"),

    path("reset/<uidb64>/<token>",
         auth_views.PasswordResetConfirmView.as_view(
             template_name="gui/password_handling/password_reset_confirm.html",
             extra_context={'user': None}),
         name="password_reset_confirm"),

    path("reset/done",
         auth_views.PasswordResetCompleteView.as_view(
             template_name="gui/password_handling/password_reset_complete.html",
             extra_context={'user': None}),
         name="password_reset_complete"),

]
