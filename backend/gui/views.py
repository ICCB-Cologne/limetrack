from django.contrib import messages
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import requires_csrf_token
from django.db import models
from django.urls import reverse
from django.forms import Field
from .forms import SampleForm, UploadForm, FilterForm, DateForm, LoginForm, SampleFormSPL
from typing import Any
from .models import HistopathologicalSample
import csv
from django.contrib.auth import authenticate, login

import pandas as pd


# Create your views here.

class SampleTrackingView(TemplateView):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_authenticated:
            messages.error(request, "Geh wo Du wohnsch, " +
                           str(request.user) + "!")
            context = {
                'form': LoginForm()
            }
            return render(request, 'gui/login.html', context=context)

        if request.user.groups.filter(name='SPL GANG GANG').exists():
            form = SampleFormSPL()
        else:
            form = SampleForm()

        template_name = 'gui/index.html'
        context = {
            'form': form,
            'upload_form': UploadForm()
        }
        return render(request, template_name, context=context)

    @method_decorator(requires_csrf_token)
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:

        # Generate auto-filled fields
        # patient_combination = request.POST['patient_identifier'] + \
        #     request.POST['recruiting_site']
        # rest_of_sample = SampleForm(patient=patient_combination)

        form: SampleForm = SampleForm(request.POST)
        if form.is_valid():

            form.save()
            messages.success(
                request, 'Submission successful!', extra_tags="general")
            return HttpResponseRedirect(request.path_info)
        else:
            messages.error(request, 'Submission unsuccessful!',
                           extra_tags="general")
            for field in form.base_fields:
                print(field)
                if field in form.errors:
                    messages.error(
                        request, form.errors[field], extra_tags=field)
                else:
                    messages.success(
                        request, "basst", extra_tags=field)
            error_message = 'Submission unsuccessful!' + form.errors.as_text()
            return render(request, 'gui/index.html', context={'form': form,
                                                              'upload_form': UploadForm()
                                                              })


class DashBoardView(TemplateView):
    def get(self, request: HttpRequest):
        template_name = 'gui/dashboard.html'
        return render(request, template_name)


class UploadView(TemplateView):
    def get(self, request: HttpRequest):
        template_name = 'gui/index.html'
        context = {
            'form': SampleForm(),
            'upload_form': UploadForm()
        }
        return render(request, template_name, context=context)

    @method_decorator(requires_csrf_token)
    def post(self, request: HttpRequest):
        template_name = 'gui/index.html'
        upload_form = UploadForm(request.POST, request.FILES)
        if upload_form.is_valid:
            self.handle_file(request.FILES["file"], request)

        return HttpResponseRedirect(reverse("config"))

    def handle_file(self, file, request):
        df = pd.read_csv(file, sep=";")
        first_error = True
        for index, row in df.iterrows():
            data = {
                "patient": row["Patient"], "identifier": "12", "patient_identifier": row["PID"], "data_sequencing_data_release": "2", "date": "12", "died": 0, "grading": "1", "localisation": "123",
                "histology_subtype": "ef", "recruiting_site": "Freiburg", "tissue_name": "asd", "sequencing_type": "sad", "reviewed_and_processed_by": "rwer", "reviewed_and_processed_by_sequencing": "34",
                "used_in": "lplp", "tissue_type": "W", "type_intervention": "ppp", "tumor_cell_content": "Sads", "spl_status": "asdsad", "tumor_cell_content_bioinf": "KKKD"
            }

            form = SampleForm(data)
            if form.is_valid():
                messages.success(
                    request, 'File upload successful!', extra_tags="file")
            else:
                if first_error == True:
                    first_error = False
                    messages.error(
                        request, "File upload fail!", extra_tags="file")

                msg = "Error in data of patient with identifier: " + \
                    str(row["PID"]) + " " + str(form.errors.as_data())
                messages.error(
                    request, msg, extra_tags="file")


class AllSamplesView(TemplateView):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        template_name = 'gui/all_samples.html'
        samples = HistopathologicalSample.objects.all()
        fields_and_values_list = [
            [(field.name, getattr(instance, field.name))
             for field in instance._meta.fields]
            for instance in samples
        ]
        filters = FilterForm()
        context = {
            'samples': fields_and_values_list,
            'filters': filters
        }
        return render(request, template_name, context=context)

    @method_decorator(requires_csrf_token)
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        delete_id = int(request.POST['id'])
        delete_instance = HistopathologicalSample.objects.get(id=delete_id)
        delete_instance.delete()
        return HttpResponseRedirect(request.path_info)


class FilteredSamplesView(TemplateView):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        template_name = 'gui/all_samples.html'
        samples = HistopathologicalSample.objects.all()
        fields_and_values_list = [
            [(field.name, getattr(instance, field.name))
             for field in instance._meta.fields]
            for instance in samples
        ]
        context = {
            'samples': fields_and_values_list,
        }
        return render(request, template_name, context=context)

    @method_decorator(requires_csrf_token)
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        template_name = 'gui/all_samples.html'
        filtered_fields = request.POST
        samples = HistopathologicalSample.objects.all()
        fields_and_values_list = [
            [(field.name, getattr(instance, field.name)) if filtered_fields[field.name] else None
             for field in instance._meta.fields]
            for instance in samples]
        context = {
            'samples': fields_and_values_list,
        }
        return render(request, template_name, context=context)


class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """
    @staticmethod
    def write(value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def some_streaming_csv_view(request):
    """A view that streams a large CSV file."""
    samples = HistopathologicalSample.objects.all()
    fields_and_values_list = [
        [(field.name, getattr(instance, field.name))
         for field in instance._meta.fields]
        for instance in samples
    ]
    rows = []
    headers = [i[0] for i in fields_and_values_list[0]]
    rows.append(headers)
    data = [[i[1] for i in sublist] for sublist in fields_and_values_list]
    data.insert(0, headers)
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    return StreamingHttpResponse(
        (writer.writerow(row) for row in data),
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="saturn3samples.csv"'},
    )


class LoginView(TemplateView):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        template_name = 'gui/login.html'
        context = {
            'form': LoginForm()
        }
        return render(request, template_name, context=context)

    @method_decorator(requires_csrf_token)
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        user_name = request.POST["user_name"]
        pw = request.POST["password"]
        user = authenticate(request, username=user_name, password=pw)
        if user is None:
            return HttpResponseRedirect(request.path_info)
        else:
            login(request, user)
            return HttpResponseRedirect(reverse("config"))
