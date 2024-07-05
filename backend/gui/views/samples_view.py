from ..forms import (
    all_field_verbose_names, field_dict,
    GroupFilterForm,

)
from ..models import HistopathologicalSample

from django.views.decorators.csrf import requires_csrf_token
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import (
    HttpRequest, HttpResponse, HttpResponseRedirect,
    StreamingHttpResponse,
)
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

import pandas as pd

from django.shortcuts import render

# from django.urls import reverse

from typing import Any
import csv

import logging

app_log = logging.getLogger("s3sample")

example_sample = [
    # recruiter
    "München", "BSP12", "f", "2021-02-10", "S3C-BSP12-0-M1-V-R1",
    "This is an example sat3 sample", "2021-02-10", "CTC",
    "Blood withdrawal", "Lung", "No", "G2",
    # tum
    "2", "15", "59", "Comment",
    # spl
    "2023-12-17", "successful RNA", "panel",
    # sclab
    "2023-12-17", "2023-12-17", "77",
    "45", "successful RNA", "ATAC",
    "Yes", "214", "123456", "123456", "Comment",
    # spatial
    "Xenium", "Xenium failed", "2023-12-19",
    "SLIDEID981", "RUNID98124234432", "PANELID98124987412",
    "2023-12-19", "RUNID98124987412", "PANELID98124987412",
    "85", "Spatial Comment",
    # lb
    "Plasma", "2023-12-17", "2023-12-17", "4", "2023-12-17",
    "111", "sequencing successful",
    # ocdf
    "pool10",
    "/omics/odcf/project/OE0130/saturn3-sc/example/example.fastq.gz",
    "/omics/odcf/example", "/omics/odcf/example", "/omics/odcf/example",
    "/omics/odcf/example", "/omics/odcf/example", "/omics/odcf/example",
    "/omics/odcf/example", "/omics/odcf/example"
    ]


class AllSamplesView(LoginRequiredMixin, TemplateView):
    def get(self, request: HttpRequest,
            *args: Any, **kwargs: Any) -> HttpResponse:
        template_name = "gui/all_samples.html"

        if len(request.GET) == 0:
            samples = HistopathologicalSample.objects.all()
            fields_and_values_list = [
                [(field.verbose_name, getattr(instance, field.name))
                    for field in instance._meta.fields]
                for instance in samples
            ]
            filters = GroupFilterForm()

        else:
            filtered_form = GroupFilterForm(request.GET)
            if filtered_form.is_valid():
                all_filters = ["id"]
                for group in filtered_form.cleaned_data:
                    all_filters += field_dict[group] \
                        if filtered_form.cleaned_data[group] else []

                samples = HistopathologicalSample.objects.all()
                fields_and_values_list = [
                    [(field.verbose_name, getattr(instance, field.name))
                        if field.name in all_filters else (None, None)
                        for field in instance._meta.fields]
                    for instance in samples]
            filters = filtered_form

        context = {
            "samples": fields_and_values_list,
            "filters": filters,
            "user": request.user  # user, not username because we
                                  # need to check the user's attributes
        }
        return render(request, template_name, context=context)

    @method_decorator(requires_csrf_token)
    def post(self, request: HttpRequest,
             *args: Any, **kwargs: Any) -> HttpResponse:
        template_name = "gui/all_samples.html"
        post_data = request.POST
        delete_id = int(post_data["id"])

        if HistopathologicalSample.objects.filter(id=delete_id).exists():
            delete_instance = HistopathologicalSample.objects.get(id=delete_id)
            delete_instance.delete()
            app_log.info(
                f"{request.user} deleted "
                f"{delete_instance.saturn3_sample_code}")

        filtered_form = GroupFilterForm(post_data)
        if filtered_form.is_valid():
            all_filters = ["id"]
            for group in filtered_form.cleaned_data:
                all_filters += field_dict[group] \
                    if filtered_form.cleaned_data[group] else []

            samples = HistopathologicalSample.objects.all()
            fields_and_values_list = [
                [(field.verbose_name, getattr(instance, field.name))
                    if field.name in all_filters else (None, None)
                    for field in instance._meta.fields]
                for instance in samples]
        filters = filtered_form

        context = {
            "samples": fields_and_values_list,
            "filters": filters,
            "user": request.user  # user, not username because we
                                  # need to check the user's attributes
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
        [(field.verbose_name, getattr(instance, field.name))
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
        headers={
            "Content-Disposition":
            'attachment; filename="saturn3samples.csv"'},
    )


def csv_template_download_csv(request):
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)

    data = [all_field_verbose_names, example_sample]
    return StreamingHttpResponse(
        (writer.writerow(row) for row in data),
        content_type="text/csv",
        headers={
            "Content-Disposition":
            'attachment; filename="saturn3samples_template.csv"'},
    )


def csv_template_download_excel(request):
    file_name = "saturn3samples_template.xlsx"
    data = [all_field_verbose_names, example_sample]
    pd.DataFrame(data[1:], columns=all_field_verbose_names). \
        to_excel(file_name,             index=False)
    with open(file_name, "rb") as fh:
        return StreamingHttpResponse(
            (line for line in fh.readlines()),
            content_type="application/vnd.ms-excel",
            headers={
                "Content-Disposition":
                f"attachment; filename={file_name}"},
        )


class FilteredDownloadView(LoginRequiredMixin, TemplateView):
    # def get(self, request: HttpRequest,
    #         *args: Any, **kwargs: Any) -> HttpResponse:
    #     return HttpResponseRedirect(reverse("all_samples"))

    def get(self, request: HttpRequest,
            *args: Any,
            **kwargs: Any) -> StreamingHttpResponse | HttpResponseRedirect:

        pseudo_buffer = Echo()

        file_type = request.GET.get("file_type")
        if file_type is None:
            return HttpResponseRedirect(request.path_info)

        form = GroupFilterForm(request.GET)
        if form.is_valid():
            all_filters = []
            for group in form.cleaned_data:
                all_filters += field_dict[group] \
                    if form.cleaned_data[group] else []

            samples = HistopathologicalSample.objects.all()
            fields_and_values_list = [
                [(field.verbose_name, getattr(instance, field.name))
                 for field in instance._meta.fields
                    if field.name in all_filters]
                for instance in samples
            ]
            rows = []
            headers = [i[0] for i in fields_and_values_list[0]]
            rows.append(headers)
            data = [[i[1] for i in sublist]
                    for sublist in fields_and_values_list]
            data.insert(0, headers)

            if file_type == "Excel":
                file_name = "saturn3samples.xlsx"
                pd.DataFrame(data[1:], columns=headers). \
                    to_excel(file_name, index=False)
                with open(file_name, 'rb') as fh:
                    response = StreamingHttpResponse(
                            (line for line in fh.readlines()),
                            content_type="application/vnd.ms-excel",
                            headers={"Content-Disposition":
                                     f"inline; filename={file_name}"})
                    return response

            elif file_type == "CSV":
                writer = csv.writer(pseudo_buffer,
                                    delimiter=",")
                content_type = "text/csv"
                file_name = "saturn3samples.csv"

                return StreamingHttpResponse(
                    (writer.writerow(row) for row in data),
                    content_type=content_type,
                    headers={"Content-Disposition":
                             f'attachment; filename="{file_name}"'})

        return HttpResponseRedirect(request.path_info)
