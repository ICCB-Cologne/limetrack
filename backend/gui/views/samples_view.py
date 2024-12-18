"""
This view handles the sample tracking table site.
For rendering the template gui/all_samples.html is utilized.

The view's post function handles deletion of entries.
The 'get' as well as the 'post' function can accept group filters within the HttpRequest as input
and return only the fields that belong to given groups.
"""


from ..forms.forms import (
    field_dict,
    GroupFilterForm,
)
from ..models import HistopathologicalSample

from django.views.decorators.csrf import requires_csrf_token
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import (
    HttpRequest, HttpResponse
)
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.shortcuts import render

# from django.urls import reverse

from typing import Any

import logging

app_log = logging.getLogger("s3sample")

def adapt_list_for_group_filter_display(key, field_list: list):
    """
    If groups want to have fields displayed in the table, that don't belong to this group these
    fields can be added here. This only works if all other groups are filtered out.
    """
    if key == "omicspath":
        field_list = field_list[:1] + ["localisation"] + field_list[1:]
    return field_list

field_dict_for_group_filters = { key: adapt_list_for_group_filter_display(key, field_dict[key]) for key in field_dict }

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

        # check which groups are checked in the filter form
        # and then only display 
        else:
            filtered_form = GroupFilterForm(request.GET)
            if filtered_form.is_valid():
                fields_and_values_list = filter_table_with_group_filter(filtered_form.cleaned_data)
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
            fields_and_values_list = filter_table_with_group_filter(filtered_form.cleaned_data)
        filters = filtered_form

        context = {
            "samples": fields_and_values_list,
            "filters": filters,
            "user": request.user  # user, not username because we
                                  # need to check the user's attributes
        }
        return render(request, template_name, context=context)


def filter_table_with_group_filter(group_filter: dict[str, Any]):
        all_filters = ["id"]
        samples = HistopathologicalSample.objects.all()

        # this part is for displaying the table with one group filter only
        # in case some groups want an individual filtering of the columns
        if sum(list(group_filter.values())) == 1:
            for group in field_dict_for_group_filters:
                    if group_filter[group]:
                        all_filters += field_dict_for_group_filters[group]
            fields_and_values_list = []
            for instance in samples:
                instance_list = []                        
                for field_name in all_filters:
                    instance_list.append(
                        (instance._meta.get_field(field_name).verbose_name, getattr(instance, field_name)))
                fields_and_values_list.append(instance_list)
        else:
            for group in group_filter:
                all_filters += field_dict[group] \
                    if group_filter[group] else []
            fields_and_values_list = [
                [(field.verbose_name, getattr(instance, field.name))
                    if field.name in all_filters else (None, None)
                    for field in instance._meta.fields]
                for instance in samples]
            
        return fields_and_values_list
