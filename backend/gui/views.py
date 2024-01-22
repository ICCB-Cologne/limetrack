from .forms import (
    SampleFormScLab, SampleFormRec, SampleFormSPL, SampleFormTUM,
    SampleFormLB, SampleForm, UploadForm, FilterForm, LoginForm,
    SearchForm
)
from .forms import (
    SampleForm, UploadForm, FilterForm, LoginForm, SampleFormSPL,
    SampleFormLB, SampleFormScLab, SampleFormTUM, SampleFormRec
)
from django.views.decorators.csrf import requires_csrf_token
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import (
    HttpRequest, HttpResponse, HttpResponseRedirect,
    StreamingHttpResponse, QueryDict
)
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.forms.models import model_to_dict
from .models import HistopathologicalSample
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse
from typing import Any
import csv

import pandas as pd
import logging
import csv

app_log = logging.getLogger("s3sample")
# app_log.info('This log is starting')
# Create your views here.


def get_form(
    group_name: str,
    data: QueryDict = None
):
    match group_name:
        case 'spl':
            form = SampleFormSPL(data=data)
        case 'tum':
            form = SampleFormTUM(data=data)
        case 'sclab':
            form = SampleFormScLab(data=data)
        case 'lb':
            form = SampleFormLB(data=data)
        case 'recruiter':
            form = SampleFormRec(data=data)
        case _:
            form = SampleForm(data=data)
    return form


class SampleTrackingView(LoginRequiredMixin, TemplateView):
    def get(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: Any
    ) -> HttpResponse:
        form = get_form(str(request.user.groups.first()).lower())
        template_name = 'gui/index.html'
        context = {
            'form': form,
            'upload_form': UploadForm(),
            'search_form': SearchForm()
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
        patient_identifier = request.POST["patient_identifier"]

        if form.is_valid():
            app_log.info(
                f'{request.user} added / edited data for patient {patient_identifier}')
            return handle_form(
                form,
                patient_identifier,
                request.POST,
                request,
                "general"
            )

        # if form is not valid: return the form with input and highlight errors red
        else:
            messages.error(
                request,
                'Submission unsuccessful!',
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
                'gui/index.html',
                context={
                    'form': form,
                    'upload_form': UploadForm()
                }
            )


# FIXME: @JG-IBSM kannst du das ggfs. aufhübschen oder wenigstens einmal durch ChatGPT jagen?
# Type hinting etc. würde mich persönlich sehr glücklich machen :)
def handle_form(form, patient_identifier, data, request, tag):
    """
    Updates existing patient records (if group membership is not recruiter)
    or creates new patient records.

    variables:
    tag = 'general' or 'file' indicating if it's submission by uploading a file or filling the form

    """
    if request.user.groups.filter(name='SPL').exists():
        spl_received = data["spl_received"]
        spl_status = data["spl_status"]
        spl_sequencing_type = data["spl_sequencing_type"]
        if HistopathologicalSample.objects.filter(patient_identifier=patient_identifier).exists():
            HistopathologicalSample.objects.filter(
                patient_identifier=patient_identifier).update(spl_received=spl_received, spl_status=spl_status,
                                                              spl_sequencing_type=spl_sequencing_type)
        else:
            messages.error(request, f'Submission unsuccessful! No patient with patient_identifier'
                                    f'{str(patient_identifier)} found.',
                           extra_tags=tag)
            return render(request, 'gui/index.html', context={'form': form,
                                                              'upload_form': UploadForm()
                                                              })

    elif request.user.groups.filter(name='TUM').exists():
        tumor_cell_content = data["tumor_cell_content"]
        if HistopathologicalSample.objects.filter(patient_identifier=patient_identifier).exists():
            HistopathologicalSample.objects.filter(
                patient_identifier=patient_identifier).update(tumor_cell_content=tumor_cell_content)
        else:
            messages.error(request, f'Submission unsuccessful! No patient with patient_identifier'
                                    f'{str(patient_identifier)} found.',
                           extra_tags=tag)
            return render(request, 'gui/index.html', context={'form': form,
                                                              'upload_form': UploadForm()
                                                              })

    elif request.user.groups.filter(name='ScLab').exists():
        sclab_received = data["sclab_received"]
        sclab_extraction_date = data["sclab_extraction_date"]
        sclab_nuclei_yield = data["sclab_nuclei_yield"]
        sclab_nuclei_size = data["sclab_nuclei_size"]
        sclab_status = data["sclab_status"]
        sclac_sequencing_type = data["sclac_sequencing_type"]
        sclab_sorting = data["sclab_sorting"]
        sclab_pool = data["sclab_pool"]
        if HistopathologicalSample.objects.filter(patient_identifier=patient_identifier).exists():
            HistopathologicalSample.objects.filter(
                patient_identifier=patient_identifier).update(
                sclab_received=sclab_received, sclab_extraction_date=sclab_extraction_date,
                sclab_nuclei_yield=sclab_nuclei_yield,
                sclab_nuclei_size=sclab_nuclei_size, sclab_status=sclab_status,
                sclac_sequencing_type=sclac_sequencing_type,
                sclab_sorting=sclab_sorting, sclab_pool=sclab_pool)
        else:
            messages.error(request, f'Submission unsuccessful! No patient with patient_identifier'
                                    f'{str(patient_identifier)} found.',
                           extra_tags=tag)
            return render(request, 'gui/index.html', context={'form': form,
                                                              'upload_form': UploadForm()
                                                              })

    elif request.user.groups.filter(name='LB').exists():
        lb_analyte_type = data["lb_analyte_type"]
        lb_sampling_date = data["lb_sampling_date"]
        lb_received = data["lb_received"]
        lb_sample_volume = data["lb_sample_volume"]
        lb_date_of_isolation = data["lb_date_of_isolation"]
        lb_total_isolated_cfdna = data["lb_total_isolated_cfdna"]
        lb_status = data["lb_status"]

        if HistopathologicalSample.objects.filter(patient_identifier=patient_identifier).exists():
            HistopathologicalSample.objects.filter(
                patient_identifier=patient_identifier).update(
                lb_analyte_type=lb_analyte_type, lb_sampling_date=lb_sampling_date, lb_received=lb_received,
                lb_sample_volume=lb_sample_volume, lb_date_of_isolation=lb_date_of_isolation,
                lb_total_isolated_cfdna=lb_total_isolated_cfdna,
                lb_status=lb_status)
        else:
            messages.error(request, f'Submission unsuccessful! No patient with patient_identifier'
                                    f'{str(patient_identifier)} found.',
                           extra_tags=tag)
            return render(request, 'gui/index.html', context={'form': form,
                                                              'upload_form': UploadForm()
                                                              })

    elif request.user.groups.filter(name='recruiter').exists():
        form.save()

    # TODO: check if user is admin
    else:
        form.save()

    if tag == "general":
        messages.success(request, 'Submission successful!', extra_tags=tag)
        return HttpResponseRedirect(request.path_info)
    else:
        return


class DashBoardView(LoginRequiredMixin, TemplateView):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        template_name = 'gui/dashboard.html'
        return render(request, template_name)


class UploadView(LoginRequiredMixin, TemplateView):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        template_name = 'gui/index.html'
        context = {
            'form': SampleForm(),
            'upload_form': UploadForm()
        }
        return render(request, template_name, context=context)

    @method_decorator(requires_csrf_token)
    def post(self, request: HttpRequest):
        upload_form = UploadForm(request.POST, request.FILES)
        if upload_form.is_valid():
            return self.handle_file(request.FILES["file"], request)

        messages.error(request, "File upload failed!", extra_tags="file")
        return HttpResponseRedirect(reverse("config"))

    def handle_file(self, file, request):
        """
        TODO: needs to be adapted to the different sorts of forms / group memberships
        """
        df = pd.read_csv(file, sep=";", keep_default_na=False)
        first_error = True
        for index, row in df.iterrows():
            data = {
                "recruiting_site": row["Recruiting Site"], "patient_identifier": row["Patient Identifier"],
                "died": row["Died"], "saturn3_sample_code": row["SATURN3 Sample Code"],
                "sampling_date": row["Sampling Date"], "tissue_type": row["Tissue Type"],
                "type_of_intervention": row["Type of Intervention"], "localisation": row["Localisation"],
                "corresponding_organoid": row["Corresponding Organoid"], "grading": row["Grading"],
                "tumor_cell_content": row["Tumor Cell Content"], "spl_received": row["SPL Received"],
                "spl_status": row["SPL Status"], "spl_sequencing_type": row["SPL Sequencing Type"],
                "sclab_recveived": row["scLab Received"], "sclab_extraction_date": row["scLab Extraction Date"],
                "sclab_nuclei_yield": row["scLab Nuclei Yield"], "sclab_nuclei_size": row["scLab Nuclei Size [µm]"],
                "sclab_status": row["scLab Status"], "sclab_sequencing_type": row["scLab Sequencing Type"],
                "sclab_sorting": row["scLab Sorting"], "sclab_pool": row["scLab Pool"],
                "lb_analyte_type": row["LB analyte type"], "lb_sampling_date": row["LB Sampling Date"],
                "lb_received": row["LB Received"], "lb_sample_volume": row["LB Sample Volume [ml]"],
                "lb_total_isolated_cfdna": row["LB Total Isolated cfDNA [ng]"], "lb_status": row["LB Status"],
                # "patient": row["Patient"], tissue_name : row["Tissue Name"], "used_in" : row[Used in], "histology_subtype": row["Histology Subtype"],
            }

            form = get_form(str(request.user.groups.first()).lower())

            if form.is_valid():
                # alternatively append ever valid form to valid_forms
                # and process them only if all forms were valid after the for loop

                handle_form(
                    form, data["patient_identifier"], data, request, "file")
            else:
                if first_error:
                    messages.error(
                        request, "File upload failed!", extra_tags="file")

                msg = f"Error in data of patient with identifier: {str(row['Patient Identifier'])}\n" \
                      f"{str(form.errors.as_text())}"
                messages.error(
                    request, msg, extra_tags="file")
                return HttpResponseRedirect(request.path_info)

        messages.success(request, "File upload successful!", extra_tags="file")
        return HttpResponseRedirect(request.path_info)


class AllSamplesView(LoginRequiredMixin, TemplateView):
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


class FilteredSamplesView(LoginRequiredMixin, TemplateView):
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


def log_out(request: HttpRequest):
    print("Hullo -----------Yasdsadasdas")
    logout(request)
    print("Hullo -----------Y___Y_Y__Y__- ")
    return HttpResponseRedirect(reverse("config"))


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


class SearchView(LoginRequiredMixin, TemplateView):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        form = get_form(str(request.user.groups.first()).lower())
        template_name = 'gui/index.html'
        context = {
            'form': form,
            'upload_form': UploadForm(),
            'search_form': SearchForm()
        }
        return render(request, template_name, context=context)

    @method_decorator(requires_csrf_token)
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        form = SearchForm(request.POST)
        search = request.POST["search_field"]

        if form.is_valid():
            if HistopathologicalSample.objects.filter(patient_identifier=search).exists():
                found_record = HistopathologicalSample.objects.get(
                    patient_identifier=search)

                model_dict = model_to_dict(found_record)
                model_dict.pop("id")
                form = SampleForm(model_dict)

                messages.success(
                    request, f"FOUND patient_identifier {search}", extra_tags="general")
                template_name = 'gui/index.html'
                context = {
                    'form': form,
                    'upload_form': UploadForm(),
                    'search_form': SearchForm()
                }
                return render(request, template_name, context=context)

            else:
                messages.error(request, f"DID NOT FIND patient_identifier {search}",
                               extra_tags="general")
                return HttpResponseRedirect(reverse("config"))

        else:
            messages.error(request, 'Invalid input',
                           extra_tags="general")
            return HttpResponseRedirect(reverse("config"))
