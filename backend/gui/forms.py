from django import forms
from django.forms import ModelForm
from .models import HistopathologicalSample, CHARFIELD_MAXLEN
from .utils.model_choices import (
                     SITE_CHOICES, SEX_CHOICES,
                     TISSUE_TYPES, INTERVENTION_TYPES,
                     GRADING,
                     CORRESPONDING_ORGANOID_CHOICES,
                     LOCALISATION_CHOICE)
from tempus_dominus.widgets import DatePicker
# documentation https://github.com/FlipperPA/django-tempus-dominus
from .utils.fields import SampleCodeField, SampleCodeWidget


all_field_verbose_names = []
all_field_names = []

# exclude primary key "ID" by indexing
# for we dont want it displayed
all_fields = HistopathologicalSample._meta.get_fields()[1:]

for field in all_fields:
    all_field_verbose_names.append(field.verbose_name)

for field in all_fields:
    # exclude odcf
    if field.name == "pools":
        break
    all_field_names.append(field.name)


# lists of fields for individual groups
# TODO: after adding new model fields
# change indexes here by changing the first
# and the last model field name of a group
recruiter_fields = all_field_names[:all_field_names.index("grading") + 1]

tum_fields = ["saturn3_sample_code"] + \
    all_field_names[
        all_field_names.index("tumor_cell_content"):
        all_field_names.index("tumor_cell_content") + 1]

spl_fields = ["saturn3_sample_code"] + \
    all_field_names[
        all_field_names.index("spl_received"):
        all_field_names.index("spl_sequencing_type") + 1]

sclab_fields = ["saturn3_sample_code"] + \
    all_field_names[
        all_field_names.index("sclab_received"):
        all_field_names.index("spatial_comment") + 1]

spatial_fields = ["saturn3_sample_code"] + \
    all_field_names[
        all_field_names.index("spatial_method"):
        all_field_names.index("spatial_comment") + 1]

lb_fields = ["saturn3_sample_code"] + \
    all_field_names[
        all_field_names.index("lb_analyte_type"):
        all_field_names.index("lb_status") + 1]

odcf_fields = ["saturn3_sample_code"] + \
    [field.name for field in all_fields[len(all_field_names):]]

field_dict = {
    "recruiter": recruiter_fields,
    "odcf": odcf_fields,
    "tum": tum_fields,
    "spl": spl_fields,
    "sclab": sclab_fields,
    "spatial": spatial_fields,
    "lb": lb_fields,
              }

# dicts for disabling (+ grey display of)
# the widgets/input fields of individual groups

disabled_tum_dict = {
    "tumor_cell_content": forms.NumberInput(
        attrs={"disabled": "true"}),
}

disabled_spl_dict = {
            "spl_received": DatePicker(
                attrs={"disabled": "true",
                       "input_group": False}),

            "spl_status": forms.Select(
                attrs={"disabled": "true"}),

            "spl_sequencing_type": forms.Select(
                attrs={"disabled": "true"}),
}

disabled_sclab_dict = {
            "sclab_received": DatePicker(
                attrs={"disabled": "true",
                       "input_group": False}),

            "sclab_extraction_date": DatePicker(
                attrs={"disabled": "true",
                       "input_group": False}),

            "sclab_nuclei_yield": forms.NumberInput(
                attrs={"disabled": "true"}),

            "sclab_nuclei_size": forms.NumberInput(
                attrs={"disabled": "true"}),

            "sclab_status": forms.TextInput(
                attrs={"disabled": "true"}),

            "sclab_sequencing_type": forms.TextInput(
                attrs={"disabled": "true"}),

            "sclab_sorting": forms.NullBooleanSelect(
                attrs={"disabled": "true"}),

            "atac_isle_id": forms.TextInput(
                attrs={"disabled": "true"}),

            "rna_isle_id": forms.TextInput(
                attrs={"disabled": "true"}),

            "sclab_pool": forms.NumberInput(
                attrs={"disabled": "true"}),

            "sclab_comment": forms.TextInput(
                attrs={"disabled": "true"}),
}

disabled_spatial_dict = {

            "spatial_method": forms.TextInput(
                attrs={"disabled": "true"}),

            "spatial_status": forms.TextInput(
                attrs={"disabled": "true"}),

            "xenium_run_date": DatePicker(
                attrs={"disabled": "true",
                       "input_group": False}),

            "xenium_slide_id": forms.TextInput(
                attrs={"disabled": "true"}),

            "xenium_run_id": forms.TextInput(
                attrs={"disabled": "true"}),

            "xenium_panel_id": forms.TextInput(
                attrs={"disabled": "true"}),

            "merscope_run_date": DatePicker(
                attrs={"disabled": "true",
                       "input_group": False}),

            "merscope_run_id": forms.TextInput(
                attrs={"disabled": "true"}),

            "merscope_panel_id": forms.TextInput(
                attrs={"disabled": "true"}),

            "dv_200": forms.TextInput(
                attrs={"disabled": "true"}),

            "spatial_comment": forms.TextInput(
                attrs={"disabled": "true"}),

}

disabled_lb_dict = {

            "lb_analyte_type": forms.Select(
                attrs={"disabled": "true"}),

            "lb_sampling_date": DatePicker(
                attrs={"disabled": "true",
                       "input_group": False}),

            "lb_received": DatePicker(
                attrs={"disabled": "true",
                       "input_group": False}),

            "lb_sample_volume": forms.NumberInput(
                attrs={"disabled": "true"}),

            "lb_date_of_isolation": DatePicker(
                attrs={"disabled": "true",
                       "input_group": False}),

            "lb_total_isolated_cfdna": forms.NumberInput(
                attrs={"disabled": "true"}),

            "lb_status": forms.Select(
                attrs={"disabled": "true"}),
}


class SampleForm(ModelForm):
    """
    For admins, coordinators & superusers
    This form allows entries in every field of the
    HistopathologicalSample model.

    The submission of this form can create new records.
    """
    required_css_class = "required"
    # error_css_class = "error-field"

    saturn3_sample_code = SampleCodeField(required=True,
                                          widget=SampleCodeWidget(),
                                          label="SATURN3 Sample Code")

    class Meta:
        model = HistopathologicalSample
        fields = all_field_names + odcf_fields

        widgets = {

            # include tooltips into widgets
            "patient_identifier": forms.TextInput(
                attrs={"data-toggle": "tooltip",
                       "data-placement": "top",
                       "title": "5-digit SATURN3 pseudonym \
                        (by Treuhandstelle Freiburg)",
                       "onchange": "autoFillPatient(this.value)"}
                       ),

            "corresponding_organoid": forms.Select(
                attrs={"data-toggle": "tooltip",
                       "data-placement": "top",
                       "title": "generated from the same biopsy/tissue piece"}
                       ),

            "dv_200": forms.TextInput(
                attrs={"data-toggle": "tooltip",
                       "data-placement": "top",
                       "title": "Quality meassure: RNA \
                        molecules larger than 200 bp [%]"}
                        ),


            # Datepicker widgets
            "died": DatePicker(
                options={"allowInputToggle": True},
                attrs={"input_group": False}),

            "sampling_date": DatePicker(
                options={"allowInputToggle": True},
                attrs={"input_group": False}),

            "spl_received": DatePicker(
                options={"allowInputToggle": True},
                attrs={"input_group": False}),

            "sclab_received": DatePicker(
                options={"allowInputToggle": True},
                attrs={"input_group": False}),

            "sclab_extraction_date": DatePicker(
                options={"allowInputToggle": True},
                attrs={"input_group": False}),

            "xenium_run_date": DatePicker(
                options={"allowInputToggle": True},
                attrs={"input_group": False}),

            "merscope_run_date": DatePicker(
                options={"allowInputToggle": True},
                attrs={"input_group": False}),

            "lb_sampling_date": DatePicker(
                options={"allowInputToggle": True},
                attrs={"input_group": False}),

            "lb_received": DatePicker(
                options={"allowInputToggle": True},
                attrs={"input_group": False}),

            "lb_date_of_isolation": DatePicker(
                options={"allowInputToggle": True},
                attrs={"input_group": False}),
        }


class SampleFormRec(ModelForm):
    """
    For recruiters only

    The submission of this form can create new records.
    """
    required_css_class = "required"
    # error_css_class = "error-field"

    saturn3_sample_code = SampleCodeField(required=True,
                                          widget=SampleCodeWidget(),
                                          label="SATURN3 Sample Code")

    class Meta:
        model = HistopathologicalSample
        fields = all_field_names

        widgets = {
            # include tooltips into widgets
            "patient_identifier": forms.TextInput(
                attrs={"data-toggle": "tooltip",
                       "data-placement": "top",
                       "title": "5-digit SATURN3 \
                        pseudonym (by Treuhandstelle Freiburg)",
                       "onchange": "autoFillPatient(this.value)"}
                       ),

            "died": DatePicker(
                options={"allowInputToggle": True},
                attrs={"input_group": False}
                ),

            "sampling_date": DatePicker(
                options={"allowInputToggle": True},
                attrs={"input_group": False}
                ),

            "corresponding_organoid": forms.Select(
                attrs={"data-toggle": "tooltip",
                       "data-placement": "top",
                       "title": "generated from the same biopsy/tissue piece"},
                       ),

        } | disabled_tum_dict | disabled_spl_dict \
            | disabled_sclab_dict | disabled_spatial_dict \
            | disabled_lb_dict


class SampleFormTUM(ModelForm):
    """
    For TUM group members only

    The submission of this form can not create new records.
    """
    required_css_class = "required"

    saturn3_sample_code = SampleCodeField(required=True,
                                          widget=SampleCodeWidget(),
                                          label="SATURN3 Sample Code")

    # set disabled required recruiter fields on not required
    recruiting_site = forms.CharField(
        max_length=CHARFIELD_MAXLEN,
        required=False,
        widget=forms.Select(
            attrs={
                "onchange": "autoFillPatient(this.value)",
                "disabled": "true"
                },
            choices=SITE_CHOICES)
        )

    patient_identifier = forms.CharField(
        max_length=5,
        required=False,
        widget=forms.TextInput(
            attrs={"data-toggle": "tooltip",
                   "data-placement": "top",
                   "data-html": "true",
                   "title": "5-digit SATURN3 \
                    pseudonym (by Treuhandstelle Freiburg)",
                   "onchange": "autoFillPatient(this.value)",
                   "disabled": "true"}))

    sex = forms.CharField(
        max_length=CHARFIELD_MAXLEN,
        required=False,
        widget=forms.Select(
            attrs={"disabled": "true"},
            choices=SEX_CHOICES))

    died = forms.DateField(
        required=False,
        widget=DatePicker(
            options={},
            attrs={"input_group": False,
                   "disabled": "true"}
                   ))

    note = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"disabled": "true"}))

    sampling_date = forms.DateField(
        required=False,
        widget=DatePicker(
            options={},
            attrs={"input_group": False,
                   "disabled": "true"}
                   ))

    tissue_type = forms.CharField(
        max_length=CHARFIELD_MAXLEN,
        required=False,
        widget=forms.Select(
            attrs={"disabled": "true"},
            choices=TISSUE_TYPES))

    type_of_intervention = forms.CharField(
        max_length=CHARFIELD_MAXLEN,
        required=False,
        widget=forms.Select(
            attrs={"disabled": "true"},
            choices=INTERVENTION_TYPES))

    localisation = forms.CharField(
        max_length=CHARFIELD_MAXLEN,
        required=False,
        widget=forms.Select(
            attrs={"disabled": "true"},
            choices=LOCALISATION_CHOICE))

    corresponding_organoid = forms.BooleanField(
        required=False,
        widget=forms.Select(
            attrs={"disabled": "true"},
            choices=CORRESPONDING_ORGANOID_CHOICES))

    grading = forms.CharField(
        max_length=CHARFIELD_MAXLEN,
        required=False,
        widget=forms.Select(
            attrs={"disabled": "true"},
            choices=GRADING))

    # end of disabling required fields

    class Meta:
        model = HistopathologicalSample
        fields = all_field_names
        widgets = {

        } | disabled_spl_dict | disabled_sclab_dict \
            | disabled_spatial_dict | disabled_lb_dict


class SampleFormSPL(SampleFormTUM):
    """
    For SPL group members only

    The submission of this form can not create new records.
    """

    class Meta:
        model = HistopathologicalSample
        fields = all_field_names
        widgets = {

            # DatePickers

            'spl_received': DatePicker(
                options={"allowInputToggle": True},
                attrs={"input_group": False}),

        } | disabled_tum_dict | disabled_sclab_dict \
            | disabled_spatial_dict | disabled_lb_dict


class SampleFormScLab(SampleFormTUM):
    """
    For ScLab group members only

    The submission of this form can not create new records.
    """

    class Meta:
        model = HistopathologicalSample

        fields = all_field_names
        widgets = {

            # tool tips
            "dv_200": forms.TextInput(
                attrs={"data-toggle": "tooltip",
                       "data-placement": "top",
                       "title": "Quality meassure: RNA \
                        molecules larger than 200 bp [%]"}
                        ),

            # DatePickers:

            'sclab_received': DatePicker(
                options={"allowInputToggle": True},
                attrs={"input_group": False}),

            'sclab_extraction_date': DatePicker(
                options={"allowInputToggle": True},
                attrs={"input_group": False}),

            "xenium_run_date": DatePicker(
                options={"allowInputToggle": True},
                attrs={"input_group": False}),

            "merscope_run_date": DatePicker(
                options={"allowInputToggle": True},
                attrs={"input_group": False}),

        } | disabled_tum_dict | disabled_spl_dict | disabled_lb_dict


class SampleFormSpatial(SampleFormTUM):
    class Meta:
        model = HistopathologicalSample

        fields = all_field_names

        widgets = {

            # tool tips
            "dv_200": forms.TextInput(
                attrs={"data-toggle": "tooltip",
                       "data-placement": "top",
                       "title": "Quality meassure: RNA \
                        molecules larger than 200 bp [%]"}
                        ),

            # date pickers
            "xenium_run_date": DatePicker(
                options={"allowInputToggle": True},
                attrs={"input_group": False}),

            "merscope_run_date": DatePicker(
                options={"allowInputToggle": True},
                attrs={"input_group": False}),

        } | disabled_tum_dict | disabled_spl_dict | disabled_lb_dict \
            | disabled_sclab_dict


class SampleFormLB(SampleFormTUM):
    """
    For LB group members only

    The submission of this form can not create new records.
    """

    class Meta:
        model = HistopathologicalSample
        fields = all_field_names
        widgets = {

            # DatePickers:

            'lb_sampling_date': DatePicker(
                options={"allowInputToggle": True},
                attrs={"input_group": False}),

            'lb_received': DatePicker(
                options={"allowInputToggle": True},
                attrs={"input_group": False}),

            'lb_date_of_isolation': DatePicker(
                options={"allowInputToggle": True},
                attrs={"input_group": False}),

        } | disabled_tum_dict | disabled_spl_dict | disabled_sclab_dict \
            | disabled_spatial_dict


class SampleFormDataPaths(SampleFormTUM):
    """
    For DataPath group members only

    The submission of this form can not create new records.
    """

    class Meta:
        model = HistopathologicalSample
        fields = all_field_names + odcf_fields
        widgets = {

        } | disabled_tum_dict | disabled_spl_dict \
            | disabled_sclab_dict | disabled_spatial_dict \
            | disabled_lb_dict


class UploadForm(forms.Form):
    file = forms.FileField()


class FilterForm(forms.Form):
    """
    Not in usage yet.
    """
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
    """
    Enables filtering of the sample tables's columns.
    """
    recruiter = forms.BooleanField(initial=True,
                                   required=False,
                                   label="Recruiter")

    tum = forms.BooleanField(initial=True,
                             required=False,
                             label="TUM")

    spl = forms.BooleanField(initial=True,
                             required=False,
                             label="SPL")

    sclab = forms.BooleanField(initial=True,
                               required=False,
                               label="ScLab")

    spatial = forms.BooleanField(initial=True,
                                 required=False,
                                 label="Spatial")

    lb = forms.BooleanField(initial=True,
                            required=False,
                            label="LB")

    odcf = forms.BooleanField(initial=True,
                              required=False,
                              label="ODCF")


class LoginForm(forms.Form):
    user_name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class SearchForm(forms.Form):
    radio_select = forms.ChoiceField(
        choices=[
            ("Patient Identifier", "SATURN3 Patient Identifier"),
            ("SATURN3 Sample Code", "SATURN3 Sample Code")],
        label="Search for",
        widget=forms.RadioSelect())

    search_field = forms.CharField(label="Search")
