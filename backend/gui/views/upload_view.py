from ..forms import (
    all_field_verbose_names, all_field_names, odcf_fields,
    UploadForm,
    SearchForm
)
from ..models import (
    HistopathologicalSample, check_sat3_sample_code,
    check_sat3_sample_code_with_none_analyte
)

from .views import (get_form, handle_form,
                    check_existing_input_for_group, record_already_exists,
                    no_sample_code_found)

from django.views.decorators.csrf import requires_csrf_token
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import (
    HttpRequest, HttpResponse, HttpResponseRedirect,
)
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from django.contrib import messages
from django.shortcuts import render
from django.forms import ModelForm
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

from typing import Any
import pandas as pd
import logging

app_log = logging.getLogger("s3sample")


class UploadView(LoginRequiredMixin, TemplateView):
    def get(self, request: HttpRequest,
            *args: Any, **kwargs: Any) -> HttpResponse:

        template_name = "gui/index.html"
        form = get_form(str(request.user.groups.first()).lower())
        context = {
            "form": form,
            "upload_form": UploadForm(),
            "search_form": SearchForm()
        }
        return render(request, template_name, context=context)

    @method_decorator(requires_csrf_token)
    def post(self, request: HttpRequest):
        upload_form = UploadForm(request.POST, request.FILES)
        if upload_form.is_valid():
            return self.handle_file(request.FILES["file"], request)

        messages.error(request, "File upload failed!", extra_tags="file")
        return HttpResponseRedirect(reverse("config"))

    @staticmethod
    def handle_file(file, request: HttpRequest):
        """
        TODO: needs to be adapted to the different
        sorts of forms / group memberships
        """

        try:
            df = pd.read_csv(file, sep=",|;", keep_default_na=False)
        except UnicodeDecodeError:
            messages.error(request, "File upload failed!", extra_tags="file")
            msg = "Cannot read file. Please make sure it is UTF-8 encoded."
            messages.error(request, msg, extra_tags="file")
            return HttpResponseRedirect(request.path_info)

        first_error = True
        valid_forms: list[ModelForm] = []
        row_number = 1
        for index, row in df.iterrows():

            data = {}
            for field_name, verbose_field_name in zip(all_field_names +
                                                      odcf_fields[1:],
                                                      all_field_verbose_names):

                value: str = row.get(verbose_field_name)

                # allowing yes and no
                # as Boolean values in file upload
                if (field_name == "corresponding_organoid" or
                        field_name == "sclab_sorting"):
                    if type(value) is not str:
                        pass
                    elif value.lower() == "yes":
                        value = True
                    elif value.lower() == "no":
                        value = False

                # JG-IBSM: unfortunately I can't figure out a better way
                # to check the sample code (as implemented below) by now
                # since the field is composed out of
                # multiple fields the usual form handling (form.is_valid())
                # leads to the SampleCodeWidget trying
                # to decompress() the field.
                # this yet leads to errors because decompress()
                # can only handle sample codes in the correct format
                if field_name == "saturn3_sample_code":
                    try:
                        check_sat3_sample_code(value)
                    except ValidationError:
                        try:
                            check_sat3_sample_code_with_none_analyte(value)
                        except ValidationError:
                            messages.error(request,
                                           "File upload failed!",
                                           extra_tags="file")
                            msg = f"Error in row {row_number + 1}: \
                            data of the record with SATURN3 Sample \
                            Code: {str(row['SATURN3 Sample Code'])} \
                            --- No valid SATURN3 Sample Code"
                            messages.error(request, msg, extra_tags="file")
                            return HttpResponseRedirect(request.path_info)

                data.update({field_name: value})

            form = get_form(str(request.user.groups.first()).lower(), data)

            if form.is_valid():
                # append every valid form to valid_forms list
                # and process them only if all forms are
                # valid

                form_data = form.cleaned_data
                sat3_code = form.cleaned_data["saturn3_sample_code"]

                possible_response = check_records_existence(request, sat3_code,
                                                            "file", form)
                # check_records_existence returns None if there are no errors
                # if it's not None it's an error response which has to
                # be returned

                if possible_response is not None:
                    return possible_response

                valid_forms.append(form)

            else:
                if first_error:
                    messages.error(
                        request, "File upload failed!", extra_tags="file")

                error_list = ""
                for key, value in form.errors.as_data().items():
                    if len(value) > 0:
                        error_list += f"{key}: {value[0]} </br>"

                msg = f"Error(s) in row {row_number + 1} of your CSV-file: \
                        The record's data with SATURN3 Sample Code \
                        *{str(row['SATURN3 Sample Code'])}* \
                        have following issues: </br>\
                        {error_list}"
                messages.error(
                    request, mark_safe(msg), extra_tags="file")
                return HttpResponseRedirect(request.path_info)

            row_number += 1

        for form in valid_forms:
            form_data = form.cleaned_data
            saturn3_sample_code = form_data["saturn3_sample_code"]
            handle_form(
                form,
                saturn3_sample_code,
                form_data,
                request,
                "file")
            app_log.info(
                f"{request.user} added / "
                f"edited data for patient "
                f"{saturn3_sample_code}")

        messages.success(request, "File upload successful!", extra_tags="file")
        return HttpResponseRedirect(request.path_info)


def check_records_existence(request: HttpRequest,
                            sat3_code: str,
                            tag: str,
                            form: ModelForm):
    """
    This function is required for handling files.
    It checks the database for a existing record with given
    SATURN3-Sample-Code.

    Returns error if record exists and user has no permission to change it.
    """

    if (request.user.groups.filter(
            name__in=["SPL", "TUM", "scOpenLab",
                      "LiquidBiopsy", "OmicsPath", "Spatial"]).exists()):

        # if data for the group specific fields already exists
        # and the user has no permission for editing
        # -> no update -> error message
        if HistopathologicalSample.objects. \
                filter(saturn3_sample_code=sat3_code).exists():

            if not request.user.has_perm("gui.change_histopathologicalsample"):
                group_name = str(request.user.groups.first()).lower()

                if check_existing_input_for_group(group_name, sat3_code):

                    return record_already_exists(request,
                                                 sat3_code,
                                                 tag, form, group_name)

        # no record with given sat3code exists &
        # these groups are not allowed to create records -> error message
        else:
            return no_sample_code_found(request, sat3_code, tag, form)

    # if record with given sat3sample already exists and
    # recruiter is not allowed to edit data -> error message
    elif request.user.groups.filter(name="Recruiter").exists():

        if (HistopathologicalSample.
                objects.filter(saturn3_sample_code=sat3_code).exists() and not
                request.user.has_perm("gui.change_histopathologicalsample")):
            messages.error(request,
                           f"File upload failed!"
                           f" Record with SATURN3 Sample Code "
                           f"{str(sat3_code)} already exists.",
                           extra_tags=tag)

            return render(request, "gui/index.html",
                          context={
                              "form": (form if tag == "general"
                                       else get_form(
                                           str(request.user.groups.
                                               first()).lower())),
                              "upload_form": UploadForm(),
                              "search_form": SearchForm(),
                              "jump_to": ("form" if tag == "general"
                                          else None)})

    # superuser, admins and coordinators are allowed to
    # overwrite all existing data -> update record
    elif (request.user.is_superuser
          or request.user.groups.filter(
              name__in=["superuser", "admins", "coordinators"]).exists()
          or request.user.has_perm("gui.change_histopathologicalsample")):
        return

    # unauthorized users -> error message
    else:
        messages.error(request,
                       "File upload failed!"
                       " Not permitted!",
                       extra_tags=tag)

        return render(request, "gui/index.html",
                      context={"form": form,
                               "upload_form": UploadForm(),
                               "search_form": SearchForm(),
                               "jump_to": ("form" if tag == "general"
                                           else None)})

    # if there is no existing data conflicting with the input data
    return
