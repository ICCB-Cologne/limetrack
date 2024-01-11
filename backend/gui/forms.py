from django import forms
from django.forms import ModelForm
from .models import HistopathologicalSample
from tempus_dominus.widgets import DatePicker


class SampleForm(ModelForm):
    # died = forms.DateField(widget=DatePicker())
    required_css_class = "required"
    error_css_class = "error-field"

    class Meta:
        model = HistopathologicalSample
        # fields must be replaced in production by a list of all fields due to security reasons
        fields = "__all__"
        widgets = {
            'recruiting_site': forms.Select(attrs={'onchange': "autoFillPatient(this.value)"}),
            'died': DatePicker(options={}, attrs={"input_group": False}),
            'sampling_date': DatePicker(options={}, attrs={"input_group": False}),
            'spl_received': DatePicker(options={}, attrs={"input_group": False}),
            'sclab_received': DatePicker(options={}, attrs={"input_group": False}),
            'sclab_extraction_date': DatePicker(options={}, attrs={"input_group": False}),
            'lb_sampling_date': DatePicker(options={}, attrs={"input_group": False}),
            'lb_received': DatePicker(options={}, attrs={"input_group": False}),
            'lb_date_of_isolation': DatePicker(options={}, attrs={"input_group": False})
        }


class SampleFormSPL(ModelForm):
    # died = forms.DateField(widget=DatePicker())
    required_css_class = "required"

    class Meta:
        model = HistopathologicalSample
        # fields must be replaced in production by a list of all fields due to security reasons
        fields = "__all__"
        widgets = {
            'patient_identifier': forms.TextInput(attrs={'disabled': "true"}),
            'died': DatePicker(options={}, attrs={"input_group": False, 'disabled': "true"}),
            'sampling_date': DatePicker(options={}, attrs={"input_group": False, 'disabled': "true"}),
            'spl_received': DatePicker(options={}, attrs={"input_group": False}),
            'sclab_received': DatePicker(options={}, attrs={"input_group": False, 'disabled': "true"}),
            'sclab_extraction_date': DatePicker(options={}, attrs={"input_group": False, 'disabled': "true"}),
            'lb_sampling_date': DatePicker(options={}, attrs={"input_group": False, 'disabled': "true"}),
            'lb_received': DatePicker(options={}, attrs={"input_group": False, 'disabled': "true"}),
            'lb_date_of_isolation': DatePicker(options={}, attrs={"input_group": False, 'disabled': "true"})
        }


class DateForm(forms.Form):
    date = forms.DateTimeField(
        widget=DatePicker()
    )


class UploadForm(forms.Form):
    file = forms.FileField()


class FilterForm(forms.Form):
    recruiting_site = forms.BooleanField(initial=True)
    patient_identifier = forms.BooleanField(initial=True)
    patient = forms.BooleanField(initial=True)
    died = forms.BooleanField(initial=True)
    tissue_name = forms.BooleanField(initial=True)
    used_in = forms.BooleanField(initial=True)
    date = forms.BooleanField(initial=True)
    tissue_type = forms.BooleanField(initial=True)
    type_intervention = forms.BooleanField(initial=True)
    localisation = forms.BooleanField(initial=True)
    grading = forms.BooleanField(initial=True)
    histology_subtype = forms.BooleanField(initial=True)
    tumor_cell_content = forms.BooleanField(initial=True)
    reviewed_and_processed_by = forms.BooleanField(initial=True)
    identifier = forms.BooleanField(initial=True)
    spl_status = forms.BooleanField(initial=True)
    sequencing_type = forms.BooleanField(initial=True)
    data_sequencing_data_release = forms.BooleanField(initial=True)
    tumor_cell_content_bioinf = forms.BooleanField(initial=True)
    reviewed_and_processed_by_sequencing = forms.BooleanField(initial=True)


class LoginForm(forms.Form):
    user_name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
