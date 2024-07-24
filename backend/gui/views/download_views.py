from ..forms import (
    all_field_verbose_names, field_dict,
    GroupFilterForm,

)
from ..models import HistopathologicalSample

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import (
    HttpRequest, HttpResponseRedirect,
    StreamingHttpResponse,
)
from django.views.generic import TemplateView
from typing import Any, Generator
from io import BytesIO

import pandas as pd

# from django.urls import reverse


import logging
import csv

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


class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """

    @staticmethod
    def write(value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def csv_template_download_csv(request):
    pseudo_buffer = Echo()
    filename = "saturn3samples_template.csv"
    data = [all_field_verbose_names, example_sample]
    writer = csv.writer(pseudo_buffer)

    return StreamingHttpResponse(
        (writer.writerow(row) for row in data),
        content_type="text/csv",
        headers={
            "Content-Disposition":
            f"attachment; filename={filename}"},
    )


def csv_template_download_excel(request):
    data = [all_field_verbose_names, example_sample]
    filename = "saturn3samples_template.xlsx"
    generator: Generator | None = None
    buffer = BytesIO()

    with BytesIO() as buffer:
        pd.DataFrame(data[1:], columns=all_field_verbose_names).to_excel(
            buffer, index=False
        )
        buffer.seek(0)
        generator = (line for line in buffer.readlines())

    return StreamingHttpResponse(
        generator,
        content_type="application/vnd.ms-excel",
        headers={
            "Content-Disposition":
            f"attachment; filename={filename}"},
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
                response: Generator | None = None
                file_name = "saturn3samples.xlsx"

                with BytesIO() as buffer:
                    pd.DataFrame(data[1:], columns=headers). \
                        to_excel(buffer, index=False)
                    buffer.seek(0)
                    response = StreamingHttpResponse(
                        (line for line in buffer.readlines()),
                        content_type="application/vnd.ms-excel",
                        headers={
                            "Content-Disposition": f"inline; filename={file_name}"
                        },
                    )

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
