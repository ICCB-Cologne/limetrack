from django import forms
from django.forms import ModelForm
from .models import (HistopathologicalSample,
                     SITE_CHOICES, SEX_CHOICES, CHARFIELD_MAXLEN,
                     TISSUE_TYPES, INTERVENTION_TYPES,
                     LOCALISATION_CHOICE, GRADING)
from tempus_dominus.widgets import DatePicker
# documentation https://github.com/FlipperPA/django-tempus-dominus
from .utils.fields import SampleCodeField, SampleCodeWidget

all_field_verbose_names = [
    "Recruiting Site",
    "Patient Identifier",
    # "Patient",
    "Sex",
    "Died",
    # "Tissue Name", skip for prototype
    # "Used in", skip for prototype
    "SATURN3 Sample Code",
    "Sampling Date",
    "Tissue Type",
    "Type of Intervention",
    "Localisation",
    "Corresponding Organoid",
    "Grading",
    "Tumor Cell Content",
    "SPL Received",
    "SPL Status",
    "SPL Sequencing Type",
    "scLab Received",
    "scLab Extraction Date",
    "scLab Nuclei Yield",
    "scLab Nuclei Size [µm]",
    "scLab Status",
    "scLab Sequencing Type",
    "scLab Sorting",
    "scLab Pool",
    "LB analyte type",
    "LB Sampling Date",
    "LB Received",
    "LB Sample Volume [ml]",
    "LB Date of Isolation",
    "LB Total Isolated cfDNA [ng]",
    "LB Status",

    "Pools",
    "scRNA R1",
    "scRNA R2",
    "scATAC R2",
    "scATAC I2",
    "WGS R1",
    "WGS R2",
    "WGS bam",
    "WGS vcf"
]

all_fields = [
    "recruiting_site",
    "patient_identifier",
    # "patient", skip for prototype
    "sex",
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
    "sclab_sequencing_type",
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

recruiter_fields = [
    "recruiting_site",
    "patient_identifier",
    # "patient", skip for prototype
    "sex",
    "died",
    # "tissue_name", skip for prototype
    # "used_in", skip for prototype
    "saturn3_sample_code",
    "sampling_date",
    "tissue_type",
    "type_of_intervention",
    "localisation",
    "corresponding_organoid",
    "grading"
]

ocdf_fields = [
    "saturn3_sample_code",
    "pools",
    "scrna_r1",
    "scrna_r2",
    "scatac_r1",
    "scatac_r2",
    "scatac_i2",
    "wgs_r1",
    "wgs_r2",
    "wgs_bam",
    "wgs_vcf"
]

tum_fields = [
    "saturn3_sample_code",
    "tumor_cell_content"
    ]

spl_fields = [
    "saturn3_sample_code",
    "spl_received",
    "spl_status",
    "spl_sequencing_type"]

sclab_fields = [
    "saturn3_sample_code",
    "sclab_received", 
    "sclab_extraction_date", 
    "sclab_nuclei_yield",
    "sclab_nuclei_size",
    "sclab_status",
    "sclab_sequencing_type",
    "sclab_sorting",
    "sclab_pool"
    ]

lb_fields = [
    "saturn3_sample_code",
    "lb_analyte_type",
    "lb_sampling_date",
    "lb_received",
    "lb_sample_volume",
    "lb_date_of_isolation",
    "lb_total_isolated_cfdna",
    "lb_status"
]

ocdf_fields = [
    "saturn3_sample_code",
    "pools",
    "scrna_r1",
    "scrna_r2",
    "scatac_r1",
    "scatac_r2",
    "scatac_i2",
    "wgs_r1",
    "wgs_r2",
    "wgs_bam",
    "wgs_vcf"
]

field_dict = {"recruiter" : recruiter_fields,
              "ocdf" : ocdf_fields,
              "tum" : tum_fields,
              "spl" : spl_fields,
              "sclab" : sclab_fields,
              "lb" : lb_fields,
              }

class SampleForm(ModelForm):
    required_css_class = "required"
    # error_css_class = "error-field"
    
    saturn3_sample_code = SampleCodeField(required=True, widget=SampleCodeWidget(), label="SATURN3 Sample Code")
    patient_identifier = forms.CharField(
        max_length=5,
        widget=forms.TextInput(attrs={"data-toggle" : "tooltip", 
                                      "data-placement" : "top",
                                      "title" : "5-digit SATURN3 pseudonym (by Treuhandstelle Freiburg)",
                                      'onchange': "autoFillPatient(this.value)"}),
        label="Patient Identifier")
    

    class Meta:
        model = HistopathologicalSample
        fields = all_fields + ocdf_fields

        
        widgets = {

            'died': DatePicker(options={"allowInputToggle" : True},
                               attrs={"input_group": False}),
            'sampling_date': DatePicker(options={"allowInputToggle" : True},
                                        attrs={"input_group": False}),
            'spl_received': DatePicker(options={"allowInputToggle" : True},
                                       attrs={"input_group": False}),
            'sclab_received': DatePicker(options={"allowInputToggle" : True},
                                         attrs={"input_group": False}),
            'sclab_extraction_date': DatePicker(options={"allowInputToggle" : True},
                                                attrs={"input_group": False}),
            'lb_sampling_date': DatePicker(options={"allowInputToggle" : True},
                                           attrs={"input_group": False}),
            'lb_received': DatePicker(options={"allowInputToggle" : True},
                                      attrs={"input_group": False}),
            'lb_date_of_isolation': DatePicker(options={"allowInputToggle" : True},
                                               attrs={"input_group": False}),
        }


class SampleFormRec(ModelForm):
    required_css_class = "required"
    # error_css_class = "error-field"

    saturn3_sample_code = SampleCodeField(required=True, widget=SampleCodeWidget(), label="SATURN3 Sample Code")
    patient_identifier = forms.CharField(
        max_length=5,
        widget=forms.TextInput(attrs={"data-toggle" : "tooltip", 
                                      "data-placement" : "top",
                                      "title" : "5-digit SATURN3 pseudonym (by Treuhandstelle Freiburg)",
                                      'onchange': "autoFillPatient(this.value)"}),
        label="Patient Identifier")

    class Meta:
        model = HistopathologicalSample
        fields = all_fields

        widgets = {
            'died': DatePicker(options={"allowInputToggle" : True}, attrs={
                "input_group": False}),
            'sampling_date': DatePicker(options={"allowInputToggle" : True}, attrs={
                "input_group": False}),

            # disabled
            "tumor_cell_content": forms.NumberInput(attrs={
                'disabled': "true"}),

            "spl_received": DatePicker(attrs={
                'disabled': "true", "input_group": False}),
            "spl_status": forms.Select(attrs={'disabled': "true"}),
            "spl_sequencing_type": forms.Select(attrs={'disabled': "true"}),

            "sclab_received": DatePicker(attrs={'disabled': "true",
                                                "input_group": False}),
            "sclab_extraction_date": DatePicker(attrs={'disabled': "true",
                                                       "input_group": False}),
            "sclab_nuclei_yield": forms.NumberInput(attrs={
                'disabled': "true"}),
            "sclab_nuclei_size": forms.NumberInput(attrs={'disabled': "true"}),
            "sclab_status": forms.TextInput(attrs={'disabled': "true"}),
            "sclab_sequencing_type": forms.TextInput(attrs={
                'disabled': "true"}),
            "sclab_sorting": forms.NullBooleanSelect(attrs={
                'disabled': "true"}),
            "sclab_pool": forms.NumberInput(attrs={'disabled': "true"}),

            "lb_analyte_type": forms.Select(attrs={'disabled': "true"}),
            "lb_sampling_date": DatePicker(attrs={'disabled': "true",
                                                  "input_group": False}),
            "lb_received": DatePicker(attrs={'disabled': "true",
                                             "input_group": False}),
            "lb_sample_volume": forms.NumberInput(attrs={'disabled': "true"}),
            "lb_date_of_isolation": DatePicker(attrs={'disabled': "true",
                                                      "input_group": False}),
            "lb_total_isolated_cfdna": forms.NumberInput(attrs={
                'disabled': "true"}),
            "lb_status": forms.Select(attrs={'disabled': "true"}),
        }


class SampleFormTUM(ModelForm):
    required_css_class = "required"

    saturn3_sample_code = SampleCodeField(required=True, widget=SampleCodeWidget(), label="SATURN3 Sample Code")
    patient_identifier = forms.CharField(
        max_length=5,
        widget=forms.TextInput(attrs={"data-toggle" : "tooltip", 
                                      "data-placement" : "top",
                                      "title" : "5-digit SATURN3 pseudonym (by Treuhandstelle Freiburg)",
                                      'onchange': "autoFillPatient(this.value)"}),
        label="Patient Identifier")
    
    # set disabled required recruiter fields on not required
    recruiting_site = forms.CharField(
        max_length=CHARFIELD_MAXLEN,
        required=False,
        widget=forms.Select(attrs={
            'onchange': "autoFillPatient(this.value)",
            'disabled': "true"},
            choices=SITE_CHOICES))
    patient_identifier = forms.CharField(
        max_length=5, required=False,
        widget=forms.TextInput(attrs={"data-toggle" : "tooltip", 
                                      "data-placement" : "top",
                                      "data-html" : "true",
                                      "title" : "5-digit SATURN3 pseudonym (by Treuhandstelle Freiburg)",
                                      'onchange': "autoFillPatient(this.value)"}))
    sex = forms.CharField(
        max_length=CHARFIELD_MAXLEN,
        required=False,
        widget=forms.Select(attrs={'disabled': "true"}, choices=SEX_CHOICES))
    sampling_date = forms.DateField(required=False, widget=DatePicker(
        options={}, attrs={"input_group": False, 'disabled': "true"}))
    tissue_type = forms.CharField(
        max_length=CHARFIELD_MAXLEN,
        required=False,
        widget=forms.Select(attrs={'disabled': "true"}, choices=TISSUE_TYPES))
    type_of_intervention = forms.CharField(
        max_length=CHARFIELD_MAXLEN,
        required=False,
        widget=forms.Select(attrs={'disabled': "true"},
                            choices=INTERVENTION_TYPES))
    localisation = forms.CharField(
        max_length=CHARFIELD_MAXLEN,
        required=False,
        widget=forms.Select(attrs={'disabled': "true"},
                            choices=LOCALISATION_CHOICE))

    corresponding_organoid = forms.BooleanField(required=False,
                                                widget=forms.
                                                CheckboxInput(attrs={
                                                    'disabled': "true"}),
                                                help_text="generated"
                                                " from the same "
                                                "biopsy/tissue piece")
    grading = forms.CharField(
        max_length=CHARFIELD_MAXLEN,
        required=False,
        widget=forms.Select(attrs={'disabled': "true"}, choices=GRADING))

    class Meta:
        model = HistopathologicalSample
        fields = all_fields
        widgets = {

            # disabled

            # 'patient_identifier': forms.TextInput(attrs={'disabled': "true"})
            # always needed(?),
            # "patient", skip for prototype
            "died": DatePicker(options={},
                               attrs={'disabled': "true",
                                      "input_group": False}),
            # "tissue_name", skip for prototype
            # "used_in", skip for prototype

            "spl_received": DatePicker(attrs={'disabled': "true",
                                              "input_group": False}),
            "spl_status": forms.Select(attrs={'disabled': "true"}),
            "spl_sequencing_type": forms.Select(attrs={'disabled': "true"}),

            "sclab_received": DatePicker(attrs={'disabled': "true",
                                                "input_group": False}),
            "sclab_extraction_date": DatePicker(attrs={'disabled': "true",
                                                       "input_group": False}),
            "sclab_nuclei_yield": forms.NumberInput(attrs={
                'disabled': "true"}),
            "sclab_nuclei_size": forms.NumberInput(attrs={'disabled': "true"}),
            "sclab_status": forms.TextInput(attrs={'disabled': "true"}),
            "sclab_sequencing_type": forms.TextInput(attrs={
                'disabled': "true"}),
            "sclab_sorting": forms.NullBooleanSelect(attrs={
                'disabled': "true"}),
            "sclab_pool": forms.NumberInput(attrs={'disabled': "true"}),

            "lb_analyte_type": forms.Select(attrs={'disabled': "true"}),
            "lb_sampling_date": DatePicker(attrs={'disabled': "true",
                                                  "input_group": False}),
            "lb_received": DatePicker(attrs={'disabled': "true",
                                             "input_group": False}),
            "lb_sample_volume": forms.NumberInput(attrs={'disabled': "true"}),
            "lb_date_of_isolation": DatePicker(attrs={'disabled': "true",
                                                      "input_group": False}),
            "lb_total_isolated_cfdna": forms.NumberInput(attrs={
                'disabled': "true"}),
            "lb_status": forms.Select(attrs={'disabled': "true"}),

        }


class SampleFormSPL(SampleFormTUM):

    class Meta:
        model = HistopathologicalSample
        fields = all_fields
        widgets = {
            'spl_received': DatePicker(options={"allowInputToggle" : True},
                                       attrs={"input_group": False,                                    
                                              }),

            # disabled:

            # 'patient_identifier':
            # forms.TextInput(attrs={'disabled': "true"}) always needed(?),
            # "patient", skip for prototype
            "died": DatePicker(options={},
                               attrs={
                                   'disabled': "true",
                                   "input_group": False}),
            # "tissue_name", skip for prototype
            # "used_in", skip for prototype

            "tumor_cell_content": forms.NumberInput(attrs={
                'disabled': "true"}),

            "sclab_received": DatePicker(attrs={
                'disabled': "true",
                "input_group": False}),

            "sclab_extraction_date": DatePicker(attrs={
                'disabled': "true",
                "input_group": False}),

            "sclab_nuclei_yield": forms.NumberInput(attrs={
                'disabled': "true"}),

            "sclab_nuclei_size": forms.NumberInput(attrs={'disabled': "true"}),

            "sclab_status": forms.TextInput(attrs={'disabled': "true"}),

            "sclab_sequencing_type": forms.TextInput(attrs={
                'disabled': "true"}),

            "sclab_sorting": forms.NullBooleanSelect(attrs={
                'disabled': "true"}),

            "sclab_pool": forms.NumberInput(attrs={'disabled': "true"}),

            "lb_analyte_type": forms.Select(attrs={'disabled': "true"}),

            "lb_sampling_date": DatePicker(attrs={
                'disabled': "true",
                "input_group": False}),

            "lb_received": DatePicker(attrs={
                'disabled': "true",
                "input_group": False}),

            "lb_sample_volume": forms.NumberInput(attrs={'disabled': "true"}),

            "lb_date_of_isolation": DatePicker(attrs={
                'disabled': "true",
                "input_group": False}),

            "lb_total_isolated_cfdna": forms.NumberInput(attrs={
                'disabled': "true"}),

            "lb_status": forms.Select(attrs={'disabled': "true"}),
        }


class SampleFormScLab(SampleFormTUM):
    
    class Meta:
        model = HistopathologicalSample

        fields = all_fields
        widgets = {
            'sclab_received': DatePicker(options={"allowInputToggle" : True}, attrs={
                "input_group": False}),

            'sclab_extraction_date': DatePicker(options={"allowInputToggle" : True}, attrs={
                "input_group": False}),

            # disabled
            # 'patient_identifier': forms.TextInput(attrs={
            # 'disabled': "true"}) always needed(?),
            # "patient", skip for prototype
            "died": DatePicker(options={},
                               attrs={
                                   'disabled': "true",
                                   "input_group": False
                                   }),
            # "tissue_name", skip for prototype
            # "used_in", skip for prototype

            "tumor_cell_content": forms.NumberInput(attrs={
                'disabled': "true"}),

            "spl_received": DatePicker(attrs={
                'disabled': "true",
                "input_group": False}),

            "spl_status": forms.Select(attrs={'disabled': "true"}),

            "spl_sequencing_type": forms.Select(attrs={'disabled': "true"}),

            "lb_analyte_type": forms.Select(attrs={'disabled': "true"}),

            "lb_sampling_date": DatePicker(attrs={'disabled': "true",
                                                  "input_group": False}),

            "lb_received": DatePicker(attrs={'disabled': "true",
                                             "input_group": False}),

            "lb_sample_volume": forms.NumberInput(attrs={'disabled': "true"}),

            "lb_date_of_isolation": DatePicker(attrs={'disabled': "true",
                                                      "input_group": False}),

            "lb_total_isolated_cfdna": forms.NumberInput(attrs={
                'disabled': "true"}),

            "lb_status": forms.Select(attrs={'disabled': "true"}),

        }


class SampleFormLB(SampleFormTUM):

    class Meta:
        model = HistopathologicalSample
        fields = all_fields
        widgets = {

            'lb_sampling_date': DatePicker(options={"allowInputToggle" : True},
                                           attrs={"input_group": False}),
            'lb_received': DatePicker(options={"allowInputToggle" : True},
                                      attrs={"input_group": False}),
            'lb_date_of_isolation': DatePicker(options={"allowInputToggle" : True},
                                               attrs={"input_group": False}),

            # disabled:

            # 'patient_identifier': forms.TextInput(attrs={'disabled': "true"})
            # always needed(?),
            # "patient", skip for prototype
            "died": DatePicker(options={}, attrs={'disabled': "true",
                                                  "input_group": False}),
            # "tissue_name", skip for prototype
            # "used_in", skip for prototype

            "tumor_cell_content": forms.NumberInput(attrs={
                'disabled': "true"}),

            "spl_received": DatePicker(attrs={'disabled': "true",
                                              "input_group": False}),

            "spl_status": forms.Select(attrs={'disabled': "true"}),

            "spl_sequencing_type": forms.Select(attrs={'disabled': "true"}),

            "sclab_received": DatePicker(attrs={'disabled': "true",
                                                "input_group": False}),

            "sclab_extraction_date": DatePicker(attrs={'disabled': "true",
                                                       "input_group": False}),

            "sclab_nuclei_yield": forms.NumberInput(attrs={
                'disabled': "true"}),

            "sclab_nuclei_size": forms.NumberInput(attrs={'disabled': "true"}),

            "sclab_status": forms.TextInput(attrs={'disabled': "true"}),

            "sclab_sequencing_type": forms.TextInput(attrs={
                'disabled': "true"}),

            "sclab_sorting": forms.NullBooleanSelect(attrs={
                'disabled': "true"}),

            "sclab_pool": forms.NumberInput(attrs={'disabled': "true"}),
        }


class SampleFormDataPaths(SampleFormTUM):

    class Meta:
        model = HistopathologicalSample
        fields = all_fields + ocdf_fields
        widgets = {

            # all disabled:
            "lb_analyte_type": forms.Select(attrs={'disabled': "true"}),

            "lb_sampling_date": DatePicker(attrs={'disabled': "true",
                                                  "input_group": False}),

            "lb_received": DatePicker(attrs={'disabled': "true",
                                             "input_group": False}),

            "lb_sample_volume": forms.NumberInput(attrs={'disabled': "true"}),

            "lb_date_of_isolation": DatePicker(attrs={'disabled': "true",
                                                      "input_group": False}),

            "lb_total_isolated_cfdna": forms.NumberInput(attrs={
                'disabled': "true"}),

            "lb_status": forms.Select(attrs={'disabled': "true"}),


            # 'patient_identifier': forms.TextInput(attrs={'disabled': "true"})
            # always needed(?),
            # "patient", skip for prototype
            "died": DatePicker(options={}, attrs={'disabled': "true",
                                                  "input_group": False}),
            # "tissue_name", skip for prototype
            # "used_in", skip for prototype

            "tumor_cell_content": forms.NumberInput(attrs={
                'disabled': "true"}),

            "spl_received": DatePicker(attrs={'disabled': "true",
                                              "input_group": False}),

            "spl_status": forms.Select(attrs={'disabled': "true"}),

            "spl_sequencing_type": forms.Select(attrs={'disabled': "true"}),

            "sclab_received": DatePicker(attrs={'disabled': "true",
                                                "input_group": False}),

            "sclab_extraction_date": DatePicker(attrs={'disabled': "true",
                                                       "input_group": False}),

            "sclab_nuclei_yield": forms.NumberInput(attrs={
                'disabled': "true"}),

            "sclab_nuclei_size": forms.NumberInput(attrs={'disabled': "true"}),

            "sclab_status": forms.TextInput(attrs={'disabled': "true"}),

            "sclab_sequencing_type": forms.TextInput(attrs={
                'disabled': "true"}),

            "sclab_sorting": forms.NullBooleanSelect(attrs={
                'disabled': "true"}),

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

class GroupFilterForm(forms.Form):
    recruiter = forms.BooleanField(initial=True, required=False)
    tum = forms.BooleanField(initial=True, required=False)
    spl = forms.BooleanField(initial=True, required=False)
    sclab = forms.BooleanField(initial=True, required=False)
    lb = forms.BooleanField(initial=True, required=False)
    ocdf = forms.BooleanField(initial=True, required=False)



class LoginForm(forms.Form):
    user_name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class SearchForm(forms.Form):
    radio_select = forms.ChoiceField(choices=[("PID", "SATURN3 Patient Identifier"), ("SATURN3 Sample Code", "SATURN3 Sample Code")], label="Search for", widget=forms.RadioSelect(attrs={"id" : "humeen"}))
    search_field = forms.CharField(label="Search")
