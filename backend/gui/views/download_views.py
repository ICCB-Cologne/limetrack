from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import (
    HttpRequest,
    HttpResponseRedirect,
    StreamingHttpResponse,
    HttpResponse,
)
from django.views.generic import TemplateView
from typing import Any, Generator, Iterable
from base64 import b64encode
from io import BytesIO
from ..forms.forms import (
    all_field_verbose_names,
)
import pandas as pd
import logging
import json
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
    "Yes", "5S9QY", "123456", "123456", "Comment",
    # spatial
    "Xenium", "Xenium failed", "2023-12-19",
    "SLIDEID981", "RUNID98124234432", "PANELID98124987412",
    "2023-12-19", "RUNID98124987412", "PANELID98124987412",
    "85", "Spatial Comment",
    # lb
    "Plasma", "2023-12-17", "2023-12-17", "4", "2023-12-17",
    "111", "sequencing successful",
    # ocdf
    "demultiplexed + QC",
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


def csv_template_download_csv(request: HttpRequest):
    pseudo_buffer = Echo()
    filename = "saturn3samples_template.csv"
    data: list[Iterable[Any]] = [all_field_verbose_names[:-1], example_sample]
    writer = csv.writer(pseudo_buffer)

    return StreamingHttpResponse(
        (writer.writerow(row) for row in data),
        content_type="text/csv",
        headers={
            "Content-Disposition":
            f"attachment; filename={filename}"},
    )

def csv_template_download_excel(request: HttpRequest):
    data = [example_sample]
    columns = all_field_verbose_names[:-1] # created at excluded
    filename = "saturn3samples_template.xlsx"
    generator: Generator | None = None
    buffer = BytesIO()

    with BytesIO() as buffer:
        pd.DataFrame(data, columns=columns).to_excel(
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
    def post(self, request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
        data = request.POST.get("data")
        file_type = request.GET.get("type", "CSV")
        
        if data:
            records: list[dict] = json.loads(data)
            df = pd.DataFrame.from_records(records)
            content_type="text/csv;base64"

            with BytesIO() as buffer:
                file_name = "saturn3samples"

                if file_type == "Excel":
                    file_name += ".xlsx"
                    content_type="text/plain;base64"
                    df.to_excel(buffer, index=False)
                
                else:
                    file_name += ".csv"
                    df.to_csv(buffer, index=False)
                
                buffer.seek(0)
                response = HttpResponse(
                    b64encode(buffer.read()),
                    content_type=content_type,
                    headers={
                        "Content-Disposition": f'attachment; filename="{file_name}"',
                        "filename": file_name
                    },
                )
                    
            return response

        return HttpResponseRedirect("/samples/")
