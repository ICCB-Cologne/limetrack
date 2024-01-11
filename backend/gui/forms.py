from django import forms
from django.forms import ModelForm
from .models import HistopathologicalSample
from tempus_dominus.widgets import DatePicker

all_fields = [
    "recruiting_site",
    "patient_identifier",
    # "patient", skip for prototype
    "died",
    # "tissue_name", skip for prototype
    # "used_in", skip for prototype
    "saturn3_sample_code",
    "sampling_date",
    "tissue_type",
    "type_of_intervention",
    "localisation",
    "corresponding_organoid",
    "grading",
    "tumor_cell_content",
    "spl_received",
    "spl_status",
    "spl_sequencing_type",
    "sclab_received",
    "sclab_extraction_date",
    "sclab_nuclei_yield",
    "sclab_nuclei_size",
    "sclab_status",
    "sclac_sequencing_type",
    "sclab_sorting",
    "sclab_pool",
    "lb_analyte_type",
    "lb_sampling_date",
    "lb_received",
    "lb_sample_volume",
    "lb_date_of_isolation",
    "lb_total_isolated_cfdna",
    "lb_status"
]


class SampleForm(ModelForm):
    # died = forms.DateField(widget=DatePicker())
    required_css_class = "required"
    error_css_class = "error-field"

    class Meta:
        model = HistopathologicalSample
        # fields must be replaced in production by a list of all fields due to security reasons
        fields = all_fields

        widgets = {
            'recruiting_site': forms.Select(attrs={'onchange': "autoFillPatient(this.value)"}),
            'died': DatePicker(options={}, attrs={"input_group": False}),
            'sampling_date': DatePicker(options={}, attrs={"input_group": False}),

            # disabled
            "tumor_cell_content": forms.NumberInput(attrs={'disabled': "true"}),

            "spl_received": DatePicker(attrs={'disabled': "true", "input_group": False}),
            "spl_status": forms.Select(attrs={'disabled': "true"}),
            "spl_sequencing_type": forms.Select(attrs={'disabled': "true"}),

            "sclab_received": DatePicker(attrs={'disabled': "true", "input_group": False}),
            "sclab_extraction_date": DatePicker(attrs={'disabled': "true", "input_group": False}),
            "sclab_nuclei_yield": forms.NumberInput(attrs={'disabled': "true"}),
            "sclab_nuclei_size": forms.NumberInput(attrs={'disabled': "true"}),
            "sclab_status": forms.TextInput(attrs={'disabled': "true"}),
            "sclac_sequencing_type": forms.TextInput(attrs={'disabled': "true"}),
            "sclab_sorting": forms.NullBooleanSelect(attrs={'disabled': "true"}),
            "sclab_pool": forms.NumberInput(attrs={'disabled': "true"}),

            "lb_analyte_type": forms.Select(attrs={'disabled': "true"}),
            "lb_sampling_date": DatePicker(attrs={'disabled': "true", "input_group": False}),
            "lb_received": DatePicker(attrs={'disabled': "true", "input_group": False}),
            "lb_sample_volume": forms.NumberInput(attrs={'disabled': "true"}),
            "lb_date_of_isolation": DatePicker(attrs={'disabled': "true", "input_group": False}),
            "lb_total_isolated_cfdna": forms.NumberInput(attrs={'disabled': "true"}),
            "lb_status": forms.Select(attrs={'disabled': "true"}),
        }


class SampleFormTUM(ModelForm):
    # died = forms.DateField(widget=DatePicker())
    required_css_class = "required"

    fields = all_fields

    class Meta:
        model = HistopathologicalSample
        # fields must be replaced in production by a list of all fields due to security reasons
        fields = all_fields
        widgets = {

            # disabled

            'recruiting_site': forms.Select(attrs={'disabled': "true"}),
            # 'patient_identifier': forms.TextInput(attrs={'disabled': "true"}) always needed(?),
            # "patient", skip for prototype
            "died": DatePicker(options={}, attrs={'disabled': "true", "input_group": False}),
            # "tissue_name", skip for prototype
            # "used_in", skip for prototype
            "saturn3_sample_code": forms.TextInput(attrs={'disabled': "true", "input_group": False}),
            "sampling_date": DatePicker(options={}, attrs={"input_group": False, 'disabled': "true"}),
            "tissue_type": forms.Select(attrs={'disabled': "true"}),
            "type_of_intervention": forms.Select(attrs={'disabled': "true"}),
            "localisation": forms.Select(attrs={'disabled': "true"}),
            "corresponding_organoid": forms.CheckboxInput(attrs={'disabled': "true"}),
            "grading": forms.Select(attrs={'disabled': "true"}),

            "spl_received": DatePicker(attrs={'disabled': "true", "input_group": False}),
            "spl_status": forms.Select(attrs={'disabled': "true"}),
            "spl_sequencing_type": forms.Select(attrs={'disabled': "true"}),

            "sclab_received": DatePicker(attrs={'disabled': "true", "input_group": False}),
            "sclab_extraction_date": DatePicker(attrs={'disabled': "true", "input_group": False}),
            "sclab_nuclei_yield": forms.NumberInput(attrs={'disabled': "true"}),
            "sclab_nuclei_size": forms.NumberInput(attrs={'disabled': "true"}),
            "sclab_status": forms.TextInput(attrs={'disabled': "true"}),
            "sclac_sequencing_type": forms.TextInput(attrs={'disabled': "true"}),
            "sclab_sorting": forms.NullBooleanSelect(attrs={'disabled': "true"}),
            "sclab_pool": forms.NumberInput(attrs={'disabled': "true"}),

            "lb_analyte_type": forms.Select(attrs={'disabled': "true"}),
            "lb_sampling_date": DatePicker(attrs={'disabled': "true", "input_group": False}),
            "lb_received": DatePicker(attrs={'disabled': "true", "input_group": False}),
            "lb_sample_volume": forms.NumberInput(attrs={'disabled': "true"}),
            "lb_date_of_isolation": DatePicker(attrs={'disabled': "true", "input_group": False}),
            "lb_total_isolated_cfdna": forms.NumberInput(attrs={'disabled': "true"}),
            "lb_status": forms.Select(attrs={'disabled': "true"}),

        }


class SampleFormSPL(ModelForm):
    # died = forms.DateField(widget=DatePicker())
    required_css_class = "required"

    fields = all_fields

    class Meta:
        model = HistopathologicalSample
        # fields must be replaced in production by a list of all fields due to security reasons
        fields = "__all__"
        widgets = {
            'spl_received': DatePicker(options={}, attrs={"input_group": False}),

            # disabled:

            'recruiting_site': forms.Select(attrs={'disabled': "true"}),
            # 'patient_identifier': forms.TextInput(attrs={'disabled': "true"}) always needed(?),
            # "patient", skip for prototype
            "died": DatePicker(options={}, attrs={'disabled': "true", "input_group": False}),
            # "tissue_name", skip for prototype
            # "used_in", skip for prototype
            "saturn3_sample_code": forms.TextInput(attrs={'disabled': "true", "input_group": False}),
            "sampling_date": DatePicker(options={}, attrs={"input_group": False, 'disabled': "true"}),
            "tissue_type": forms.Select(attrs={'disabled': "true"}),
            "type_of_intervention": forms.Select(attrs={'disabled': "true"}),
            "localisation": forms.Select(attrs={'disabled': "true"}),
            "corresponding_organoid": forms.CheckboxInput(attrs={'disabled': "true"}),
            "grading": forms.Select(attrs={'disabled': "true"}),

            "tumor_cell_content": forms.NumberInput(attrs={'disabled': "true"}),

            "sclab_received": DatePicker(attrs={'disabled': "true", "input_group": False}),
            "sclab_extraction_date": DatePicker(attrs={'disabled': "true", "input_group": False}),
            "sclab_nuclei_yield": forms.NumberInput(attrs={'disabled': "true"}),
            "sclab_nuclei_size": forms.NumberInput(attrs={'disabled': "true"}),
            "sclab_status": forms.TextInput(attrs={'disabled': "true"}),
            "sclac_sequencing_type": forms.TextInput(attrs={'disabled': "true"}),
            "sclab_sorting": forms.NullBooleanSelect(attrs={'disabled': "true"}),
            "sclab_pool": forms.NumberInput(attrs={'disabled': "true"}),

            "lb_analyte_type": forms.Select(attrs={'disabled': "true"}),
            "lb_sampling_date": DatePicker(attrs={'disabled': "true", "input_group": False}),
            "lb_received": DatePicker(attrs={'disabled': "true", "input_group": False}),
            "lb_sample_volume": forms.NumberInput(attrs={'disabled': "true"}),
            "lb_date_of_isolation": DatePicker(attrs={'disabled': "true", "input_group": False}),
            "lb_total_isolated_cfdna": forms.NumberInput(attrs={'disabled': "true"}),
            "lb_status": forms.Select(attrs={'disabled': "true"}),


        }


class SampleFormScLab(ModelForm):
    # died = forms.DateField(widget=DatePicker())
    required_css_class = "required"

    fields = all_fields

    class Meta:
        model = HistopathologicalSample
        # fields must be replaced in production by a list of all fields due to security reasons
        fields = "__all__"
        widgets = {
            'sclab_received': DatePicker(options={}, attrs={"input_group": False}),
            'sclab_extraction_date': DatePicker(options={}, attrs={"input_group": False}),


            'recruiting_site': forms.Select(attrs={'disabled': "true"}),
            # 'patient_identifier': forms.TextInput(attrs={'disabled': "true"}) always needed(?),
            # "patient", skip for prototype
            "died": DatePicker(options={}, attrs={'disabled': "true", "input_group": False}),
            # "tissue_name", skip for prototype
            # "used_in", skip for prototype
            "saturn3_sample_code": forms.TextInput(attrs={'disabled': "true", "input_group": False}),
            "sampling_date": DatePicker(options={}, attrs={"input_group": False, 'disabled': "true"}),
            "tissue_type": forms.Select(attrs={'disabled': "true"}),
            "type_of_intervention": forms.Select(attrs={'disabled': "true"}),
            "localisation": forms.Select(attrs={'disabled': "true"}),
            "corresponding_organoid": forms.CheckboxInput(attrs={'disabled': "true"}),
            "grading": forms.Select(attrs={'disabled': "true"}),

            "tumor_cell_content": forms.NumberInput(attrs={'disabled': "true"}),

            "spl_received": DatePicker(attrs={'disabled': "true", "input_group": False}),
            "spl_status": forms.Select(attrs={'disabled': "true"}),
            "spl_sequencing_type": forms.Select(attrs={'disabled': "true"}),

            "lb_analyte_type": forms.Select(attrs={'disabled': "true"}),
            "lb_sampling_date": DatePicker(attrs={'disabled': "true", "input_group": False}),
            "lb_received": DatePicker(attrs={'disabled': "true", "input_group": False}),
            "lb_sample_volume": forms.NumberInput(attrs={'disabled': "true"}),
            "lb_date_of_isolation": DatePicker(attrs={'disabled': "true", "input_group": False}),
            "lb_total_isolated_cfdna": forms.NumberInput(attrs={'disabled': "true"}),
            "lb_status": forms.Select(attrs={'disabled': "true"}),

        }


class SampleFormLB(ModelForm):
    # died = forms.DateField(widget=DatePicker())
    required_css_class = "required"

    fields = all_fields

    class Meta:
        model = HistopathologicalSample
        # fields must be replaced in production by a list of all fields due to security reasons
        fields = "__all__"
        widgets = {
            'lb_sampling_date': DatePicker(options={}, attrs={"input_group": False}),
            'lb_received': DatePicker(options={}, attrs={"input_group": False}),
            'lb_date_of_isolation': DatePicker(options={}, attrs={"input_group": False}),

            # disabled:

            'recruiting_site': forms.Select(attrs={'disabled': "true"}),
            # 'patient_identifier': forms.TextInput(attrs={'disabled': "true"}) always needed(?),
            # "patient", skip for prototype
            "died": DatePicker(options={}, attrs={'disabled': "true", "input_group": False}),
            # "tissue_name", skip for prototype
            # "used_in", skip for prototype
            "saturn3_sample_code": forms.TextInput(attrs={'disabled': "true", "input_group": False}),
            "sampling_date": DatePicker(options={}, attrs={"input_group": False, 'disabled': "true"}),
            "tissue_type": forms.Select(attrs={'disabled': "true"}),
            "type_of_intervention": forms.Select(attrs={'disabled': "true"}),
            "localisation": forms.Select(attrs={'disabled': "true"}),
            "corresponding_organoid": forms.CheckboxInput(attrs={'disabled': "true"}),
            "grading": forms.Select(attrs={'disabled': "true"}),

            "tumor_cell_content": forms.NumberInput(attrs={'disabled': "true"}),

            "spl_received": DatePicker(attrs={'disabled': "true", "input_group": False}),
            "spl_status": forms.Select(attrs={'disabled': "true"}),
            "spl_sequencing_type": forms.Select(attrs={'disabled': "true"}),

            "sclab_received": DatePicker(attrs={'disabled': "true", "input_group": False}),
            "sclab_extraction_date": DatePicker(attrs={'disabled': "true", "input_group": False}),
            "sclab_nuclei_yield": forms.NumberInput(attrs={'disabled': "true"}),
            "sclab_nuclei_size": forms.NumberInput(attrs={'disabled': "true"}),
            "sclab_status": forms.TextInput(attrs={'disabled': "true"}),
            "sclac_sequencing_type": forms.TextInput(attrs={'disabled': "true"}),
            "sclab_sorting": forms.NullBooleanSelect(attrs={'disabled': "true"}),
            "sclab_pool": forms.NumberInput(attrs={'disabled': "true"}),
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
