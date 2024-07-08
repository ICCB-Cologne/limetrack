from ..forms import (
    all_field_names, odcf_fields, field_dict,
    SampleFormScLab, SampleFormRec,
    SampleFormSPL, SampleFormTUM, SampleFormLB, SampleForm,
    UploadForm, LoginForm,
    SearchForm, SampleFormDataPaths, SampleFormSpatial
)
from ..models import HistopathologicalSample

from django.views.decorators.csrf import requires_csrf_token
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import (
    HttpRequest, HttpResponse, HttpResponseRedirect,
    QueryDict
)
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.forms.models import model_to_dict
from django.contrib import messages
from django.shortcuts import render
from django.forms import ModelForm
from django.urls import reverse

from typing import Any


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
        case "spatial":
            form = SampleFormSpatial(data=data)
        case _:
            form = SampleForm(data=data)
    return form


def check_existing_input_for_group(group_name: str, sat3_code: str) -> bool:
    """
    Checks whether a group's specific fields already has entries.
    """
    record = HistopathologicalSample.objects. \
        filter(saturn3_sample_code=sat3_code).first()

    existing_fields = record._meta.get_fields()
    already_filled = False
    for field in existing_fields:
        if (field.name in field_dict[group_name][1:]
                and getattr(record, field.name) is not None
                and getattr(record, field.name) != ""):  # for TextArea fields
            already_filled = True
            break
    return already_filled


def update_record(request: HttpRequest,
                  form, group_name: str,
                  data: dict, sat3_code: str, tag: str):
    """
    Updates existing records in the db or returns error.

    If record with given sat3_code exists:
    Allows users to fill in data in the empty fields of their respective group.
    Edits a record's fields if the user has the permission to edit
    """
    update_dict = {}
    if group_name != "recruiter":
        for field in field_dict[group_name][1:]:
            update_dict.update({field: data[field]})
    else:
        for field in field_dict[group_name]:
            update_dict.update({field: data[field]})

    if (HistopathologicalSample.
            objects.filter(saturn3_sample_code=sat3_code).exists()):

        if (not request.user.has_perm("gui.change_histopathologicalsample") and
                check_existing_input_for_group(group_name, sat3_code)):

            return record_already_exists(request,
                                         sat3_code, tag, form, group_name)

        HistopathologicalSample.objects.filter(
            saturn3_sample_code=sat3_code).update(
            **update_dict)

        if tag == "general":
            messages.success(request, "Submission successful!", extra_tags=tag)
            return HttpResponseRedirect(request.path_info)

    else:
        return no_sample_code_found(request, sat3_code, tag, form)


def no_sample_code_found(request: HttpRequest,
                         sat3_code: str,
                         tag: str,
                         form: ModelForm) -> HttpResponse:
    """
    Returns HttpResponse with error message stating that a
    input with given sat3_code is not possible.
    """

    if tag == "file":
        msg = f"File upload failed!" \
            " No record with SATURN3 Sample Code " \
            f"{str(sat3_code)} found."

    else:
        msg = f"Submission unsuccessful!" \
            " No record with SATURN3 Sample Code " \
            f"{str(sat3_code)} found."

    messages.error(request,
                   msg,
                   extra_tags=tag)

    return render(request, "gui/index.html",
                  context={"form": (form if tag == "general"
                                    else get_form(
                                        str(request.user.groups
                                            .first()).lower())),
                           "upload_form": UploadForm(),
                           "search_form": SearchForm(),
                           "jump_to": ("form" if tag == "general" else None)})


def record_already_exists(request: HttpRequest, sat3_code: str,
                          tag: str, form, group_name: str) -> HttpResponse:
    """
    Returns HttpResponse with error message stating that a
    input with given sat3_code is not possible.
    """
    if tag == "file":
        fail = "File upload failed!"
    else:
        fail = "Submission unsuccessful!"

    msg = f"{fail} {group_name} data for " \
        "record with SATURN3 Sample Code " \
        f"{str(sat3_code)} already exists."

    messages.error(request,
                   msg,
                   extra_tags=tag)

    return render(request, "gui/index.html",
                  context={"form": (form if tag == "general"
                                    else get_form(str(
                                        request.user.groups.first()).lower())),
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


def handle_form(form: ModelForm,
                sat3_code: str,
                data: dict[str: Any],
                request: HttpRequest,
                tag: str):
    """
    Updates existing patient records
    or creates new patient records
    depending on user group and user permissions.

    variables:
    tag = "general" or "file"
    indicating if it's submission by uploading
    a file or filling in the form

    """
    if request.user.groups.filter(
        name__in=["SPL", "TUM", "LiquidBiopsy",
                  "scOpenLab",
                  "OmicsPath", "Spatial"]).exists():

        return update_record(request, form,
                             request.user.groups.first().name.lower(),
                             data, sat3_code, tag)

    elif request.user.groups.filter(name="Recruiter").exists():

        if (HistopathologicalSample.
            objects.filter(
                saturn3_sample_code=sat3_code).exists()):

            if request.user.has_perm("gui.change_histopathologicalsample"):
                return update_record(request, form,
                                     "recruiter", data, sat3_code, tag)

            else:
                messages.error(request,
                               "Submission unsuccessful!"
                               " Record with SATURN3 Sample Code "
                               f"{str(sat3_code)} already exists.",
                               extra_tags=tag)

                return render(request, "gui/index.html",
                              context={"form": form,
                                       "upload_form": UploadForm(),
                                       "search_form": SearchForm(),
                                       "jump_to": ("form" if tag == "general"
                                                   else None)})
        if tag == "general":
            form.save()
        else:
            # this is important for the file upload since
            # handle_file() also takes fields from the
            # csv file which do not belong to the
            # group of the uploading user.
            # Thus form.save() would also save fields
            # that must not be filled by the recruiter group

            update_dict = {}
            for field in field_dict["recruiter"]:
                update_dict.update({field: data[field]})

            HistopathologicalSample.objects.filter(
               saturn3_sample_code=sat3_code).create(
                **update_dict)

    elif (request.user.is_superuser
          or request.user.groups.filter(
              name__in=["superuser", "admins", "coordinators"]).exists()):

        if (HistopathologicalSample.
                objects.filter(saturn3_sample_code=sat3_code).exists()):
            update_dict = {}
            for field in all_field_names + odcf_fields:
                update_dict.update({field: data[field]})

            HistopathologicalSample.objects.filter(
                saturn3_sample_code=sat3_code).update(
                **update_dict)

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
        return render(
                request,
                "gui/index.html",
                context={
                    "jump_to": "form",
                    "form": get_form(str(request.user.groups.first()).lower()),
                    "upload_form": UploadForm(),
                    "search_form": SearchForm()
                }
            )
    else:
        # if a CSV file's been submitted
        return


def log_out(request: HttpRequest):
    logout(request)
    return HttpResponseRedirect(reverse("config"))


class LoginView(TemplateView):
    def get(self, request: HttpRequest,
            *args: Any, **kwargs: Any) -> HttpResponse:
        template_name = "gui/login.html"
        context = {
            "form": LoginForm(),
            "user": request.user.get_username()
        }
        return render(request, template_name, context=context)

    @method_decorator(requires_csrf_token)
    def post(self, request: HttpRequest,
             *args: Any, **kwargs: Any) -> HttpResponse:
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
    def get(self, request: HttpRequest,
            *args: Any, **kwargs: Any) -> HttpResponse:
        form = get_form(str(request.user.groups.first()).lower())
        template_name = "gui/index.html"
        context = {
            "form": form,
            "upload_form": UploadForm(),
            "search_form": SearchForm()
        }
        return render(request, template_name, context=context)

    @method_decorator(requires_csrf_token)
    def post(self, request: HttpRequest,
             *args: Any, **kwargs: Any) -> HttpResponse:
        search_form = SearchForm(request.POST)

        if search_form.is_valid():
            search = search_form.cleaned_data["search_field"]
            radio_select = search_form.cleaned_data["radio_select"]
            if (HistopathologicalSample.
                    objects.filter(saturn3_sample_code=search).exists()):

                found_record = HistopathologicalSample. \
                    objects.get(saturn3_sample_code=search)
                model_dict = model_to_dict(found_record)
                model_dict.pop("id")
                form = get_form(
                    str(request.user.groups.first()).lower(), model_dict)

            elif (HistopathologicalSample.
                    objects.filter(patient_identifier=search).exists()):

                found_records = HistopathologicalSample. \
                    objects.filter(patient_identifier=search)
                found_record = found_records[0]

                model_dict = model_to_dict(found_record)
                model_dict.pop("id")

                for key in model_dict:
                    if key not in ["recruiting_site", "patient_identifier",
                                   "sex", "died"]:
                        model_dict[key] = ""

                form = get_form(str(request.user.groups.first()).lower(),
                                model_dict)

            else:
                messages.error(request,
                               f"DID NOT FIND {radio_select} {search}",
                               extra_tags="general")
                return HttpResponseRedirect(reverse("config"))

            messages.success(
                request,
                f"FOUND {radio_select} {search}", extra_tags="general")
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
