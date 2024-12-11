from ..models import HistopathologicalSample, CHARFIELD_MAXLEN
from ..utils.fields import SampleCodeField, SampleCodeWidget
from ..utils.model_choices import (
                     SITE_CHOICES, SEX_CHOICES,
                     TISSUE_TYPES, INTERVENTION_TYPES,
                     GRADING,
                     CORRESPONDING_ORGANOID_CHOICES,
                     LOCALISATION_CHOICE)
from tempus_dominus.widgets import DatePicker #type: ignore
from django.forms import ModelForm
from django import forms
# documentation https://github.com/FlipperPA/django-tempus-dominus


all_field_verbose_names = []
all_field_names = []

# exclude primary key "ID" by indexing -> not indexing, but slicing
# for we dont want it displayed
all_fields = HistopathologicalSample._meta.get_fields()[1:]

for field in all_fields:
    all_field_verbose_names.append(field.verbose_name)

for field in all_fields:
    # exclude odcf
    if field.name == "sc_analysis_status":
        break
    all_field_names.append(field.name)


# lists of fields for individual groups
# TODO: after adding new model fields
# change indexes here by changing the first
# and the last model field name of a group
recruiter_fields = all_field_names[:all_field_names.index("grading") + 1]

tum_fields = ["saturn3_sample_code"] + \
    all_field_names[
        all_field_names.index("tissue_quality"):
        all_field_names.index("comment_tumor_cell_content") + 1]

# spl group is allowed to fill spl & tum fields
spl_fields = ["saturn3_sample_code"] + \
    all_field_names[
        all_field_names.index("tissue_quality"):
        all_field_names.index("spl_sequencing_type") + 1]

# sclab group is allowed permissions to fill sclab & spatial fields
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
    [field.name for field in all_fields[len(all_field_names):-1]]

field_dict = {
    "recruiter": recruiter_fields,
    "omicspath": odcf_fields,
    "tum": tum_fields,
    "spl": spl_fields,
    "scopenlab": sclab_fields,
    "spatial": spatial_fields,
    "liquidbiopsy": lb_fields,
              }

# dicts for disabling (+ grey display of)
# the widgets/input fields of individual groups

disabled_tum_dict = {
    tum_fields[i]: forms.TextInput(
        attrs={"disabled": "true"}) for i in range(1, len(tum_fields))
}

disabled_spl_dict = {
    spl_fields[i]: forms.TextInput(
        attrs={"disabled": "true"}) for i in range(1, len(spl_fields))
}

disabled_sclab_dict = {
    sclab_fields[i]: forms.TextInput(attrs={"disabled": "true"})
    for i in range(1, len(sclab_fields) - len(spatial_fields) + 1)
}

disabled_spatial_dict = {
    spatial_fields[i]: forms.TextInput(
        attrs={"disabled": "true"}) for i in range(1, len(spatial_fields))
}

disabled_lb_dict = {
    lb_fields[i]: forms.TextInput(
        attrs={"disabled": "true"}) for i in range(1, len(lb_fields))
}

def adapt_list_for_group_filter_display(key, list):
    """
    If groups want to have fields displayed in the table, that don't belong to the group these
    fields kan be added here
    """
    if key == "ODCF":
        list.append("location")
    return list 

field_dict_for_group_filters = { key: adapt_list_for_group_filter_display(key, field_dict[key]) for key in field_dict }



class SampleForm(ModelForm):
    """
    For admins, coordinators & superusers
    This form allows entries in every field of the
    HistopathologicalSample model.

    The submission of this form can create new records.
    """
    required_css_class = "required"
    # error_css_class = "error-field"

    saturn3_sample_code = SampleCodeField(
        required=True, widget=SampleCodeWidget(), label="SATURN3 Sample Code"
    )

    class Meta:
        model = HistopathologicalSample
        # exclude = ["id"]
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

            # widgets with additional features
            "tissue_quality": forms.NumberInput(
                attrs={'min':0, 'max': 5, 'type': 'number'}
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
        widget=forms.TextInput(
            attrs={
                "disabled": "true"
                },
            )
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
        widget=forms.TextInput(
            attrs={"disabled": "true"},
            ))

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
        widget=forms.TextInput(
            attrs={"disabled": "true"},
            ))

    type_of_intervention = forms.CharField(
        max_length=CHARFIELD_MAXLEN,
        required=False,
        widget=forms.TextInput(
            attrs={"disabled": "true"},
            ))

    localisation = forms.CharField(
        max_length=CHARFIELD_MAXLEN,
        required=False,
        widget=forms.TextInput(
            attrs={"disabled": "true"},
            ))

    corresponding_organoid = forms.BooleanField(
        required=False,
        widget=forms.TextInput(
            attrs={"disabled": "true"},
            ))

    grading = forms.CharField(
        max_length=CHARFIELD_MAXLEN,
        required=False,
        widget=forms.TextInput(
            attrs={"disabled": "true"},
            ))
    

    # end of disabling required fields

    class Meta:
        model = HistopathologicalSample
        fields = all_field_names
        widgets = {
                "tissue_quality": forms.NumberInput(
                attrs={'min':0, 'max': 5, 'type': 'number'}
            ),

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

        } | disabled_sclab_dict \
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


class SampleFormLBRecruiter(SampleFormRec):
    """
    Temporal form to enable a specific LB User to create samples
    """ 

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

        } | disabled_tum_dict | disabled_spl_dict \
            | disabled_sclab_dict | disabled_spatial_dict
    


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
        

class SampleFormReadOnly(SampleFormTUM):
    """
    Only for ReadOnly group members.
    Basically a form with disabled fields only.
    """

    saturn3_sample_code = SampleCodeField(required=True,
                                          widget=SampleCodeWidget(disabled=True),
                                          label="SATURN3 Sample Code")

    class Meta:
        model = HistopathologicalSample
        fields = all_field_names
        widgets = {

        } | disabled_tum_dict | disabled_spl_dict \
            | disabled_sclab_dict | disabled_spatial_dict \
            | disabled_lb_dict


class UploadForm(forms.Form):
    file = forms.FileField(help_text="Upload '.csv' or '.xlsx' files.", allow_empty_file=False)


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

    scopenlab = forms.BooleanField(initial=True,
                                   required=False,
                                   label="ScLab")

    spatial = forms.BooleanField(initial=True,
                                 required=False,
                                 label="Spatial")

    liquidbiopsy = forms.BooleanField(initial=True,
                                      required=False,
                                      label="LB")

    omicspath = forms.BooleanField(initial=True,
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
