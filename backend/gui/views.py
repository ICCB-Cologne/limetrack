from .forms import (
    all_field_verbose_names, all_field_names, odcf_fields, field_dict,
    SampleFormScLab, SampleFormRec,
    SampleFormSPL, SampleFormTUM, SampleFormLB, SampleForm,
    UploadForm, LoginForm, GroupFilterForm,
    SearchForm, SampleFormDataPaths,
)
from django.views.decorators.csrf import requires_csrf_token
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import (
    HttpRequest, HttpResponse, HttpResponseRedirect,
    StreamingHttpResponse, QueryDict
)
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.forms.models import model_to_dict
from .models import HistopathologicalSample, check_sat3_sample_code
from django.contrib import messages
from django.shortcuts import render
from django.forms import ModelForm
from django.urls import reverse
from django.core.exceptions import ValidationError

from typing import Any
import csv
import pandas as pd
import logging

app_log = logging.getLogger("s3sample")

# Create your views here.


def get_form(
        group_name: str,
        data: QueryDict = None
):
    match group_name.lower():
        case "spl":
            form = SampleFormSPL(data=data)
        case "tum":
            form = SampleFormTUM(data=data)
        case "scopenlab":
            form = SampleFormScLab(data=data)
        case "liquidbiopsy":
            form = SampleFormLB(data=data)
        case "recruiter":
            form = SampleFormRec(data=data)
        case "omicspath":
            form = SampleFormDataPaths(data=data)
        case _:
            form = SampleForm(data=data)
    return form


def check_existing_input_for_group(group_name: str, sat3_code: str) -> bool:
    # temporary auxiliary dictionairy -
    # remove after refractoring all old user group names to the new ones
    temp_dict = {"spl": "spl",
                 "tum": "tum",
                 "scopenlab": "sclab",
                 "liquidbiopsy": "lb",
                 "omicspath": "odcf"
                 }
    if group_name in temp_dict.keys():
        group_name = temp_dict[group_name]

    record = HistopathologicalSample.objects. \
        filter(saturn3_sample_code=sat3_code).first()

    existing_fields = record._meta.get_fields()
    already_filled = False
    for field in existing_fields:
        if (field.name in field_dict[group_name][1:]
                and getattr(record, field.name) is not None
                and getattr(record, field.name) != ""):  # for TextArea fields ...
            already_filled = True
            break
    return already_filled


def check_records_existence(request: HttpRequest,
                            sat3_code: str,
                            tag: str,
                            form: ModelForm):

    if (request.user.groups.filter(name="SPL").exists() or
        request.user.groups.filter(name="TUM").exists() or
        request.user.groups.filter(name="scOpenLab").exists() or
        request.user.groups.filter(name="LiquidBiopsy").exists() or
            request.user.groups.filter(name="OmicsPath").exists()):

        # if data for the group specific fields already exists -> no update -> error message
        if HistopathologicalSample.objects. \
                filter(saturn3_sample_code=sat3_code).exists():
            group_name = str(request.user.groups.first()).lower()
            if check_existing_input_for_group(group_name, sat3_code):
                return record_already_exists(request, sat3_code, tag, form, group_name)

        # no record with given sat3code exists -> these groups are not allowed to create records -> error message
        else:
            return no_sample_code_found(request, sat3_code, tag, form)

    # if record with given sat3sample already exists -> recruiter is not allowed to edit data -> error message
    elif request.user.groups.filter(name="Recruiter").exists():
        if HistopathologicalSample.objects.filter(saturn3_sample_code=sat3_code).exists():
            messages.error(request,
                           f"File upload failed!"
                           f" Record with saturn3_sample_code "
                           f"{str(sat3_code)} already exists.",
                           extra_tags=tag)

            return render(request, "gui/index.html",
                          context={"form": (form if tag == "general" else get_form(str(request.user.groups.first()).lower())),
                                   "upload_form": UploadForm(),
                                   "search_form": SearchForm(),
                                   "jump_to": ("form" if tag == "general" else None)})

    # superuser, admins and coordinators are allowed to overwrite all existing data -> update and create records
    elif (request.user.is_superuser
          or request.user.groups.filter(name="superuser").exists()
          or request.user.groups.filter(name="admins").exists()
          or request.user.groups.filter(name="coordinators").exists()
          ):
        return

    # unauthorized users -> error message
    else:
        messages.error(request,
                       f"File upload failed!"
                       f" Not permitted!",
                       extra_tags=tag)

        return render(request, "gui/index.html",
                      context={"form": form,
                               "upload_form": UploadForm(),
                               "search_form": SearchForm(),
                               "jump_to": ("form" if tag == "general"
                                           else None)})

    # if there is no existing data conflicting with the input data
    return


def update_record(request: HttpRequest, form, group_name: str, data: dict, sat3_code: str, tag: str):
    update_dict = {}
    for field in field_dict[group_name][1:]:
        update_dict.update({field: data[field]})

    if HistopathologicalSample.objects.filter(saturn3_sample_code=sat3_code).exists():

        if check_existing_input_for_group(group_name, sat3_code):
            return record_already_exists(request, sat3_code, tag, form, group_name)

        HistopathologicalSample.objects.filter(
            saturn3_sample_code=sat3_code).update(
            **update_dict)

        if tag == "general":
            messages.success(request, "Submission successful!", extra_tags=tag)
        return HttpResponseRedirect(request.path_info)

    else:
        return no_sample_code_found(request, sat3_code, tag, form)


def no_sample_code_found(request: HttpRequest, sat3_code: str, tag: str, form: ModelForm):

    if tag == "file":
        msg = f"File upload failed!" \
            " No record with saturn3_sample_code " \
            f"{str(sat3_code)} found."

    else:
        msg = f"Submission unsuccessful!" \
            " No record with saturn3_sample_code " \
            f"{str(sat3_code)} found."

    messages.error(request,
                   msg,
                   extra_tags=tag)

    return render(request, "gui/index.html",
                  context={"form": (form if tag == "general" else get_form(str(request.user.groups.first()).lower())),
                           "upload_form": UploadForm(),
                           "search_form": SearchForm(),
                           "jump_to": ("form" if tag == "general" else None)})


def record_already_exists(request: HttpRequest, sat3_code: str, tag: str, form, group_name: str):

    if tag == "file":
        msg = f"File upload failed! {group_name} data for " \
            "record with saturn3_sample_code " \
            f"{str(sat3_code)} already exists."

    else:
        msg = f"Submission unsuccessful! {group_name} data for " \
            "record with saturn3_sample_code " \
            f"{str(sat3_code)} already exists."

    messages.error(request,
                   msg,
                   extra_tags=tag)

    return render(request, "gui/index.html",
                  context={"form": (form if tag == "general" else get_form(str(request.user.groups.first()).lower())),
                           "upload_form": UploadForm(),
                           "search_form": SearchForm(),
                           "jump_to": ("form" if tag == "general" else None)})


class SampleTrackingView(LoginRequiredMixin, TemplateView):
    def get(
            self,
            request: HttpRequest,
            *args: Any,
            **kwargs: Any
    ) -> HttpResponse:
        form = get_form(str(request.user.groups.first()).lower())
        template_name = "gui/index.html"
        context = {
            "form": form,
            "upload_form": UploadForm(),
            "search_form": SearchForm(),
            "user": request.user.get_username()
        }

        return render(request, template_name, context=context)

    @method_decorator(requires_csrf_token)
    def post(
            self,
            request: HttpRequest,
            *args: Any,
            **kwargs: Any
    ) -> HttpResponse:
        form = get_form(str(request.user.groups.first()).lower(), request.POST)

        if form.is_valid():
            data = form.cleaned_data
            saturn3_sample_code = data["saturn3_sample_code"]
            app_log.info(
                f"{request.user} added / "
                f"edited data for patient "
                f"{saturn3_sample_code}")

            return handle_form(
                form,
                saturn3_sample_code,
                data,
                request,
                "general"
            )

        # if form is not valid:
        # return the form with input and highlight errors red
        else:
            messages.error(
                request,
                "Submission unsuccessful!",
                extra_tags="general"
            )

            for field in form.base_fields:
                if field in form.errors:
                    messages.error(
                        request,
                        form.errors[field],
                        extra_tags=field
                    )
                else:
                    messages.success(
                        request,
                        "Success!",
                        extra_tags=field
                    )
            return render(
                request,
                "gui/index.html",
                context={
                    "jump_to": "form",
                    "form": form,
                    "upload_form": UploadForm(),
                    "search_form": SearchForm()
                }
            )


# FIXME: @JG-IBSM kannst du das ggfs. aufhübschen oder wenigstens einmal durch ChatGPT jagen?
# Type hinting etc. würde mich persönlich sehr glücklich machen :)
def handle_form(form: ModelForm,
                sat3_code: str,
                data: dict[str: Any],
                request: HttpRequest,
                tag: str):
    """
    Updates existing patient records (if group membership is not recruiter)
    or creates new patient records (if group membership is recruiter).

    variables:
    tag = "general" or "file"
    indicating if it's submission by uploading
    a file or filling in the form

    """
    if request.user.groups.filter(name="SPL").exists():

        return update_record(request, form, "spl", data, sat3_code, tag)

    elif request.user.groups.filter(name="TUM").exists():

        return update_record(request, form, "tum", data, sat3_code, tag)

    elif request.user.groups.filter(name="scOpenLab").exists():

        return update_record(request, form, "sclab", data, sat3_code, tag)

    elif request.user.groups.filter(name="LiquidBiopsy").exists():

        return update_record(request, form, "lb", data, sat3_code, tag)

    elif request.user.groups.filter(name="OmicsPath").exists():

        return update_record(request, form, "odcf", data, sat3_code, tag)

    elif request.user.groups.filter(name="Recruiter").exists():
        # maybe check if record already exists and deny creating of new record
        if HistopathologicalSample.objects.filter(saturn3_sample_code=sat3_code).exists():
            messages.error(request,
                           f"Submission unsuccessful!"
                           f" Record with saturn3_sample_code "
                           f"{str(sat3_code)} already exists.",
                           extra_tags=tag)

            return render(request, "gui/index.html",
                          context={"form": form,
                                   "upload_form": UploadForm(),
                                   "search_form": SearchForm(),
                                   "jump_to": ("form" if tag == "general" else None)})
        if tag == "general":
            form.save()
        else:
            update_dict = {}
            for field in field_dict["recruiter"]:
                update_dict.update({field: data[field]})

            HistopathologicalSample.objects.filter(
               saturn3_sample_code=sat3_code).create(
                **update_dict
            )

    elif (request.user.is_superuser
          or request.user.groups.filter(name="superuser").exists()
          or request.user.groups.filter(name="admins").exists()
          or request.user.groups.filter(name="coordinators").exists()
          ):

        if HistopathologicalSample.objects.filter(saturn3_sample_code=sat3_code).exists():
            update_dict = {}
            for field in all_field_names + odcf_fields:
                update_dict.update({field: data[field]})

            HistopathologicalSample.objects.filter(
                saturn3_sample_code=sat3_code).update(
                **update_dict
            )
            # messages.error(request,
            #                f"Submission unsuccessful!"
            #                f" Record with saturn3_sample_code "
            #                f"{str(sat3_code)} already exists.",
            #                extra_tags=tag)

            # return render(request, "gui/index.html",
            #               context={"form": form,
            #                        "upload_form": UploadForm(),
            #                        "search_form": SearchForm(),
            #                        "jump_to": ("form" if tag == "general"
            #                                    else None)})

        else:
            form.save()

    else:
        messages.error(request,
                       "Submission unsuccessful!"
                       " Not permitted!",
                       extra_tags=tag)

        return render(request, "gui/index.html",
                      context={"form": form,
                               "upload_form": UploadForm(),
                               "search_form": SearchForm(),
                               "jump_to": ("form" if tag == "general"
                                           else None)})

    if tag.lower() == "general":
        # if form's been input by using the webpages form
        messages.success(request, "Submission successful!", extra_tags=tag)
        return HttpResponseRedirect(request.path_info)
    else:
        # if a CSV file's been submitted
        return


class DashBoardView(LoginRequiredMixin, TemplateView):
    def get(self, request: HttpRequest,
            *args: Any, **kwargs: Any) -> HttpResponse:
        template_name = "gui/dashboard.html"
        return render(request, template_name)


class ContactView(LoginRequiredMixin, TemplateView):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        template_name = "gui/contact.html"
        return render(request, template_name)


class ImprintView(TemplateView):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        template_name = "gui/imprint.html"
        context = {
            "user": request.user.get_username()
        }

        return render(request, template_name, context=context)


class UploadView(LoginRequiredMixin, TemplateView):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
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

        df = pd.read_csv(file, sep=",", keep_default_na=False)
        first_error = True
        valid_forms: list[ModelForm] = []
        row_number = 1
        for index, row in df.iterrows():

            data = {}
            for field_name, verbose_field_name in zip(all_field_names + odcf_fields[1:], all_field_verbose_names):
                value: str = row.get(verbose_field_name)

                # workaround for allowing yes and no as Boolean values in file upload
                if field_name == "corresponding_organoid" or field_name == "sclab_sorting":
                    if type(value) is not str:
                        pass
                    elif value.lower() == "yes":
                        value = True
                    elif value.lower() == "no":
                        value = False

                # unfortunately I can't figure out a better way to check the sample code (as implemented below) by now
                # since the field is composed out of multiple fields the usual form handling (form.is_valid())
                # leads to the SampleCodeWidget trying to decompress() the field.
                # this yet leads to errors because decompress() can only handle sample codes in the
                # correct format
                if field_name == "saturn3_sample_code":
                    try:
                        check_sat3_sample_code(value)
                    except ValidationError:
                        messages.error(request, "File upload failed!", extra_tags="file")
                        msg = f"Error in row {row_number + 1}: data of the record with SATURN3 Sample Code: {str(row['SATURN3 Sample Code'])} --- No valid SATURN3 Sample Code"
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

                possible_response = check_records_existence(request, sat3_code, "file", form)

                # check_records_existence with returns None if there are no errors
                # if it's not None it's an error response which has to
                # be returned
                if possible_response is not None:
                    return possible_response

                valid_forms.append(form)

            else:
                if first_error:
                    messages.error(
                        request, "File upload failed!", extra_tags="file")

                msg = f"Error in row {row_number + 1}: data of the record with SATURN3 Sample Code: {str(row['SATURN3 Sample Code'])} --- {str(form.errors.as_text())}"
                messages.error(
                    request, msg, extra_tags="file")
                return HttpResponseRedirect(request.path_info)

            row_number += 1

        for form in valid_forms:
            form_data = form.cleaned_data
            handle_form(
                form,
                form_data["saturn3_sample_code"],
                form_data,
                request,
                "file")

        messages.success(request, "File upload successful!", extra_tags="file")
        return HttpResponseRedirect(request.path_info)


class ConfirmSubmissionView(LoginRequiredMixin, TemplateView):
    pass


class AllSamplesView(LoginRequiredMixin, TemplateView):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        template_name = "gui/all_samples.html"
        samples = HistopathologicalSample.objects.all()
        fields_and_values_list = [
            [(field.verbose_name, getattr(instance, field.name))
             for field in instance._meta.fields]
            for instance in samples
        ]

        filters = GroupFilterForm()
        context = {
            "samples": fields_and_values_list,
            "filters": filters,
            "user": request.user  # user, not username because we need to check the user's attributes
        }
        return render(request, template_name, context=context)

    @method_decorator(requires_csrf_token)
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        delete_id = int(request.POST["id"])
        delete_instance = HistopathologicalSample.objects.get(id=delete_id)
        delete_instance.delete()
        app_log.info(
            f"{request.user} deleted "
            f"{delete_instance.saturn3_sample_code}")
        return HttpResponseRedirect(request.path_info)


class FilteredSamplesView(LoginRequiredMixin, TemplateView):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        template_name = "gui/all_samples.html"
        samples = HistopathologicalSample.objects.all()
        fields_and_values_list = [
            [(field.verbose_name, getattr(instance, field.name))
             for field in instance._meta.fields]
            for instance in samples
        ]
        filters = GroupFilterForm()
        context = {
            "samples": fields_and_values_list,
            "filters": filters
        }
        return render(request, template_name, context=context)

    @method_decorator(requires_csrf_token)
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        template_name = "gui/all_samples.html"
        filtered_form = GroupFilterForm(request.POST)
        if filtered_form.is_valid():
            all_filters = []
            for group in filtered_form.cleaned_data:
                all_filters += field_dict[group] if filtered_form.cleaned_data[group] else []

            samples = HistopathologicalSample.objects.all()
            fields_and_values_list = [
                [(field.verbose_name, getattr(instance, field.name)) if field.name in all_filters else (None, None)
                 for field in instance._meta.fields]
                for instance in samples
            ]

            context = {
                "samples": fields_and_values_list,
                "filters": filtered_form
            }
            return render(request, template_name, context=context)

        return HttpResponseRedirect(request.path_info)


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
        headers={"Content-Disposition": 'attachment; filename="saturn3samples.csv"'},
    )


def csv_template_download(request):
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    return StreamingHttpResponse(
        (writer.writerow(all_field_verbose_names)),
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="saturn3template.csv"'},
    )


class FilteredDownloadView(LoginRequiredMixin, TemplateView):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return HttpResponseRedirect(reverse("all_samples"))

    @method_decorator(requires_csrf_token)
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> StreamingHttpResponse | HttpResponseRedirect:
        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)

        form = GroupFilterForm(request.POST)
        if form.is_valid():
            all_filters = []
            for group in form.cleaned_data:
                all_filters += field_dict[group] if form.cleaned_data[group] else []

            samples = HistopathologicalSample.objects.all()
            fields_and_values_list = [
                [(field.verbose_name, getattr(instance, field.name))
                 for field in instance._meta.fields if field.name in all_filters]
                for instance in samples
            ]
            rows = []
            headers = [i[0] for i in fields_and_values_list[0]]
            rows.append(headers)
            data = [[i[1] for i in sublist] for sublist in fields_and_values_list]
            data.insert(0, headers)

            return StreamingHttpResponse(
                (writer.writerow(row) for row in data),
                content_type="text/csv",
                headers={"Content-Disposition": 'attachment; filename="saturn3samples.csv"'}, )

        return HttpResponseRedirect(request.path_info)


def log_out(request: HttpRequest):
    logout(request)
    return HttpResponseRedirect(reverse("config"))


class LoginView(TemplateView):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        template_name = "gui/login.html"
        context = {
            "form": LoginForm(),
            "user": request.user.get_username()
        }
        return render(request, template_name, context=context)

    @method_decorator(requires_csrf_token)
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        user_name = request.POST["user_name"]
        pw = request.POST["password"]
        user = authenticate(request, username=user_name, password=pw)
        if user is None:
            messages.error(
                        request, "Wrong password or user name.")
            return HttpResponseRedirect(request.path_info)
        else:
            login(request, user)
            return HttpResponseRedirect(reverse("config"))


class SearchView(LoginRequiredMixin, TemplateView):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        form = get_form(str(request.user.groups.first()).lower())
        template_name = "gui/index.html"
        context = {
            "form": form,
            "upload_form": UploadForm(),
            "search_form": SearchForm()
        }
        return render(request, template_name, context=context)

    @method_decorator(requires_csrf_token)
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        search_form = SearchForm(request.POST)

        if search_form.is_valid():
            search = search_form.cleaned_data["search_field"]
            radio_select = search_form.cleaned_data["radio_select"]
            if HistopathologicalSample.objects.filter(saturn3_sample_code=search).exists():
                found_record = HistopathologicalSample.objects.get(saturn3_sample_code=search)

                model_dict = model_to_dict(found_record)
                model_dict.pop("id")

                form = get_form(str(request.user.groups.first()).lower(), model_dict)

            elif HistopathologicalSample.objects.filter(patient_identifier=search).exists():
                found_records = HistopathologicalSample.objects.filter(patient_identifier=search)
                found_record = found_records[0]

                model_dict = model_to_dict(found_record)
                model_dict.pop("id")

                for key in model_dict:
                    if key not in ["recruiting_site", "patient_identifier", "sex", "died"]:
                        model_dict[key] = ""

                form = get_form(str(request.user.groups.first()).lower(), model_dict)

            else:
                messages.error(request, f"DID NOT FIND {radio_select} {search}",
                               extra_tags="general")
                return HttpResponseRedirect(reverse("config"))

            messages.success(
                request, f"FOUND {radio_select} {search}", extra_tags="general")
            template_name = "gui/index.html"
            context = {
                "jump_to": "form",
                "form": form,
                "upload_form": UploadForm(),
                "search_form": SearchForm()
            }

            return render(request, template_name, context=context)

        else:
            messages.error(request, "Invalid input",
                           extra_tags="general")
            return HttpResponseRedirect(reverse("config"))
