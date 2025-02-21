from django.views.decorators.csrf import requires_csrf_token
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.uploadedfile import UploadedFile
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView
from ...settings import FILE_TRACEBACK_DIR
from django.shortcuts import render
from django.contrib import messages
from django.forms import ModelForm
from django.urls import reverse
from django.http import (
    HttpResponseRedirect,
    HttpRequest,
    HttpResponse,
)
from ..utils.permission_manager import get_all_permitted_fields
from typing import Any
from ..models import (
    HistopathologicalSample,
    check_sat3_sample_code_with_none_analyte,
    check_sat3_sample_code,
)

from .views import (
    check_existing_input_for_group, 
    check_existing_entries,
    record_already_exists,
    get_form, handle_form,
    no_sample_code_found
)
from ..forms.forms import (
    all_field_verbose_names,
    field_dict,
    all_field_names,
    UploadForm,
    SearchForm
)
from pathlib import Path
from time import time
import pandas as pd
from os import path
import logging

app_log = logging.getLogger("s3sample")


class UploadView(LoginRequiredMixin, TemplateView):
    def get(self, request: HttpRequest,
            *args: Any, **kwargs: Any) -> HttpResponse:

        template_name = "gui/sample_tracking.html"
        form = get_form(request.user)
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
            try:
                return self.handle_file(request.FILES["file"], request)
            except TypeError:
                messages.error(request, "File upload failed!",
                               extra_tags="file")
                msg = "Cannot read file. Please make sure your data \
                    is separated by commas and all required fields are \
                    filled out properly (i.e. correct data type etc)."
                messages.error(request, msg, extra_tags="file")
                return HttpResponseRedirect(request.path_info)
        
        messages.error(request, "File upload failed!", extra_tags="file")
        msg = "Cannot read file. Invalid file extension. Allowed extensions are .csv & .xlsx"
        messages.error(request, msg, extra_tags="file")
        return HttpResponseRedirect(reverse("sample_tracking"))
    
    def save_file(self, file: pd.DataFrame, request: HttpRequest):
        storage_dir = Path(FILE_TRACEBACK_DIR)
        username: str = request.user.username # type: ignore

        if not storage_dir.exists():
            storage_dir.mkdir()

        filename = f"{username}_{int(time())}.upload"
        filepath = storage_dir / filename
        counter = 0

        while filepath.exists():
            filename = f"{filename}.{counter}"
            filepath = storage_dir / filename

        file.to_csv(filepath)

    def handle_file(self, file: UploadedFile, request: HttpRequest):
        """
        Here the uploaded csv/excel file is processed line by line.
        Every line e.g. sample is checked for errors. If an error is detected,
        an error message is displayed with information about the error and where
        to find the record with the erroneous data.

        Changes to the database are made only if all samples are correct.
        """
        file_ending = file.name.split(".")[-1]

        try:
            match file_ending:
                case "xlsx":
                    df = pd.read_excel(file, keep_default_na=False)
                case _:
                    df = pd.read_csv(file, sep=",", keep_default_na=False,
                                     # na_values= [""],
                                     dtype=str)

        except UnicodeDecodeError:
            messages.error(request, "File upload failed!", extra_tags="file")
            msg = "Cannot read file. Please make sure your file \
                   is a UTF-8 encoded CSV file."
            messages.error(request, msg, extra_tags="file")
            return HttpResponseRedirect(request.path_info)

        self.save_file(df, request)
        
        first_error = True
        valid_forms: list[ModelForm] = []
        row_number = 1
        for index, row in df.iterrows():

            data = {}
            for field_name, verbose_field_name in zip(all_field_names,
                                                      all_field_verbose_names):
                

                value: str = row.get(verbose_field_name)

                # allowing yes and no
                # as Boolean values in file upload
                # TODO: probably can be deleted
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

            # put the data of each line into a form
            form = get_form(request.user, data)

            if form.is_valid():
                # append every valid form to valid_forms list
                # and process them only if all forms are
                # valid

                form_data = form.cleaned_data
                sat3_code = form.cleaned_data["saturn3_sample_code"]

                user = request.user

                user_permissions = user.get_all_permissions()
                if "histopathological_sample.readonly" in user_permissions:
                    messages.error(request,
                       "File upload failed!"
                       " Not permitted!")

                    return render(request, "gui/sample_tracking.html",
                      context={"form": form,
                               "upload_form": UploadForm(),
                               "search_form": SearchForm(),})


                permitted_fields = get_all_permitted_fields(user)
                update_dict = {}

                for field in permitted_fields:
                    update_dict.update({field: data[field]}) 
                
                
                possible_response = check_records_existence(request, sat3_code,
                                                            "file", form, update_dict)
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

        # the actual handling of the valid records
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
                            form: ModelForm,
                            update_dict: dict):
    """
    This function is required for handling files.
    It checks the database for a existing record with given
    SATURN3-Sample-Code.

    Returns error if record exists and user has no permission to change it.
    Or returns error if users with no permission to create records try to upload non-existent
    Sample Codes
    """

    # unauthorized users -> error message
    if len(request.user.get_all_permissions()) == 0:
            messages.error(request,
                       "File upload failed!"
                       " Not permitted!",
                       extra_tags=tag)
            
            return render(request, "gui/sample_tracking.html",
                      context={"form": form,
                               "upload_form": UploadForm(),
                               "search_form": SearchForm(),
                               "jump_to": ("form" if tag == "general"
                                           else None)})

    if (HistopathologicalSample.
            objects.filter(saturn3_sample_code=sat3_code).exists()):
                
        # no editing permissions and filled data fields -> error message
        if(not request.user.has_perm("gui.change_histopathologicalsample")):
            if (check_existing_entries(request.user, sat3_code, update_dict)):
                return record_already_exists(request, sat3_code, "file", form, request.user.groups.first())
        
    else:

        # no permission to create -> error message
        if not request.user.has_perm("gui.add_histopathologicalsample"):
            return no_sample_code_found(request, sat3_code, tag, form)
        
    # if there is no existing data conflicting with the input data
    return
