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

from backend.gui.views import SampleTrackingView, FilteredSamplesView, AllSamplesView, some_streaming_csv_view, UploadView, DashBoardView, LoginView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", SampleTrackingView.as_view(), name="config"),
    path("#endofpage", SampleTrackingView.as_view(), name="endofpage"),
    path("samples/", AllSamplesView.as_view(), name="all_samples"),
    path("samples/filtered", FilteredSamplesView.as_view(), name="filtered_samples"),
    path("csv/", some_streaming_csv_view, name="csv"),
    path("upload/", UploadView.as_view(), name="upload"),
    path("dashboard/", DashBoardView.as_view(), name="dashboard"),
    path("login/", LoginView.as_view(), name="login"),
]
