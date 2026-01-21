"""
This view handles the sample tracking table site.
For rendering the template gui/all_samples.html is utilized.

The view's post function handles deletion of entries.
The 'get' as well as the 'post' function can accept
group filters within the HttpRequest as input
and return only the fields that belong to given groups.
"""
import ast
import logging

from ..forms.forms import (
    field_dict,
    GroupFilterForm,
)
from ..models import HistopathologicalSample

from django.db.models.functions import Substr
from django.views.decorators.csrf import requires_csrf_token
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import (
    HttpRequest, HttpResponse
)
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.shortcuts import render
from typing import Any

app_log = logging.getLogger("s3sample")

# Lists of data fields for the column filters that are not filtering model
# sections but custom views of the table.
column_filters_no_group = {
    "scmultiome": ["sclab_pool", "s3_bucket_status",
                   "scrna_r1", "scrna_r2",
                   "scatac_r1", "scatac_r2", "scatac_i2"],
    "wgs": ["wgs_r1", "wgs_r2", "wgs_bam", "wgs_vcf", "wgs_ref"],
    "variantcalling": ["wgs_r1", "wgs_r2", "wgs_bam", "wgs_ref"]
}


def adapt_list_for_group_filter_display(key, field_list: list):
    """
    Custom group filters
    If groups want to have fields displayed in the table,
    that don't belong to this group these fields can be added here.
    This only works if all other groups are filtered out.
    """
    if key == "omicspath":
        field_list = field_list[:1] + ["localisation"] + field_list[1:]
    return field_list


field_dict_for_group_filters = {key: adapt_list_for_group_filter_display(
    key, field_dict[key]) for key in field_dict} | column_filters_no_group


class SomeSamplesView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        column_names = ast.literal_eval(
            request.GET.get("column_names")
        )

        limit = 100
        offset = int(request.GET.get("offset", 0))
        subset = slice(offset, offset + limit)

        verbose_to_field = {
            field.verbose_name: field.name
            for field in HistopathologicalSample._meta.get_fields()
            if hasattr(field, "verbose_name")
        }

        field_names = [
            verbose_to_field[cn] for cn in column_names
        ]
        samples = list(
            HistopathologicalSample.objects.values(*field_names)[subset]
        )
        has_more = len(samples) == limit

        print(type(samples))

        context = {
            "samples": samples,
            "next_offset": offset + limit if has_more else None,
            "column_names": column_names,
        }

        return render(request, "gui/partials/table_row.html", context)


class AllSamplesView(LoginRequiredMixin, TemplateView):
    def get(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        template_name = "gui/all_samples.html"
        column_names = []
        num_samples = HistopathologicalSample.objects.count()
        num_patients = HistopathologicalSample.objects.annotate(
            patient_code=Substr("saturn3_sample_code", 4, 5)
        ).values("patient_code").distinct().count()

        if len(request.GET) == 0:
            if num_samples > 0:
                first_sample = HistopathologicalSample.objects.first()
                column_names = [
                    field.verbose_name
                    for field in first_sample._meta.fields
                ]
            filters = GroupFilterForm()
        else:
            filtered_form = GroupFilterForm(request.GET)
            if filtered_form.is_valid():
                column_names = get_filtered_column_names(
                    filtered_form.cleaned_data
                )
            filters = filtered_form

        context = {
            "num_samples": num_samples,
            "num_patients": num_patients,
            "column_names": column_names,
            "filters": filters,
            "user": request.user
        }
        return render(request, template_name, context=context)

    @method_decorator(requires_csrf_token)
    def post(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
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
        num_samples = HistopathologicalSample.objects.count()
        num_patients = HistopathologicalSample.objects.annotate(
            patient_code=Substr("saturn3_sample_code", 4, 5)
        ).values("patient_code").distinct().count()

        column_names = []
        if filtered_form.is_valid():
            column_names = get_filtered_column_names(
                filtered_form.cleaned_data
            )
        filters = filtered_form

        context = {
            "column_names": column_names,
            "num_samples": num_samples,
            "num_patients": num_patients,
            "filters": filters,
            "user": request.user
        }
        return render(request, template_name, context=context)


def get_filtered_column_names(group_filter: dict[str, Any]):
    if HistopathologicalSample.objects.count() == 0:
        return []

    # If recruiter_fields are filtered out, we need to display sample code
    # explicitly.
    all_filters = (
        ["id"] if group_filter["recruiter"] else ["id", "saturn3_sample_code"]
    )
    first_sample = HistopathologicalSample.objects.first()

    # This part is for displaying the table with one group filter only
    # in case some groups want an individual filtering of the columns.
    if sum(list(group_filter.values())) == 1:
        for group in field_dict_for_group_filters:
            if group_filter[group]:
                all_filters += field_dict_for_group_filters[group]
    else:
        for group in group_filter:
            all_filters += field_dict_for_group_filters[group] \
                if group_filter[group] else []

    column_names = []
    for field_name in all_filters:
        column_names.append(
            first_sample._meta.get_field(field_name).verbose_name
        )

    return column_names
