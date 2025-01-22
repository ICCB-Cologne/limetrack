from ..models import HistopathologicalSample, CHARFIELD_MAXLEN
from ..utils.fields import SampleCodeField, SampleCodeWidget
from ..utils.model_choices import (
                     SITE_CHOICES, SEX_CHOICES,
                     TISSUE_TYPES, INTERVENTION_TYPES,
                     GRADING,
                     CORRESPONDING_ORGANOID_CHOICES,
                     LOCALISATION_CHOICE)
from ..utils.model_to_form import(
    create_date_picker_dicts
)
from tempus_dominus.widgets import DatePicker #type: ignore
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
# documentation https://github.com/FlipperPA/django-tempus-dominus


all_field_verbose_names = []
all_field_names = []
date_pickers = {}

# exclude primary key "ID" by indexing -> not indexing, but slicing
# for we dont want it displayed
all_fields = HistopathologicalSample._meta.get_fields()[1:]

for field in all_fields:
    all_field_verbose_names.append(field.verbose_name)
    if field.get_internal_type() == "DateField":
        date_pickers.update(
            {field.name : DatePicker(
                options={"allowInputToggle": True},
                attrs={"input_group": False})
                })

for field in all_fields:
    # exclude odcf
    if field.name == "request_execution_of":
        break
    all_field_names.append(field.name)


# lists of fields for individual groups
# TODO: after adding new model fields
# if necessary
# change indexes here by changing the first
# and the last model field name of a group

# recruiter fields: from 'recruiting_site' to 'grading'
recruiter_fields = all_field_names[:all_field_names.index("grading") + 1]

# tum fields: from 'tissue_quality' to 'comment_tumor_cell_content'
tum_fields = ["saturn3_sample_code"] + \
    all_field_names[
        all_field_names.index("tissue_quality"):
        all_field_names.index("comment_tumor_cell_content") + 1]

spl_fields = ["saturn3_sample_code"] + \
    all_field_names[
        all_field_names.index("spl_received"):
        all_field_names.index("spl_sequencing_type") + 1]

# sclab group is allowed permissions to fill sclab & spatial fields
sclab_fields = ["saturn3_sample_code"] + \
    all_field_names[
        all_field_names.index("sclab_received"):
        all_field_names.index("sclab_comment") + 1]

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
    "tum": tum_fields,
    "spl": spl_fields,
    "scopenlab": sclab_fields,
    "spatial": spatial_fields,
    "liquidbiopsy": lb_fields,
    "omicspath": odcf_fields,
              }

# dicts for disabling (+ grey display of)
# the widgets/input fields of individual groups
# here we only have the groups "original" fields
# not additional, e.g. disabled_spl_dict has only disabled spl fields 
# and no tum fields included 

disabled_tum_dict = {
    tum_fields[i]: forms.TextInput(
        attrs={"disabled": "true"}) for i in range(1, len(tum_fields))
}

disabled_spl_dict = {
    spl_fields[i]: forms.TextInput(
        attrs={"disabled": "true"}) 
        for i in range(len(tum_fields), len(spl_fields))
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


# date picker dicts for each group
recruiter_date_pickers, tum_date_pickers, \
    spl_date_pickers, sclab_date_pickers, \
        spatial_date_pickers, lb_date_pickers, \
              odcf_date_pickers = create_date_picker_dicts(date_pickers, field_dict)


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
        } | date_pickers


class FlexibleSampleForm(ModelForm):
    """
    This form disables fields depending on the permissions a user has. 
    Only works for users with permissons to create records.
    """
    required_css_class = "required"
    # error_css_class = "error-field"

    saturn3_sample_code = SampleCodeField(
        required=True, widget=SampleCodeWidget(), label="SATURN3 Sample Code")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.disable_widgets(user)

    def disable_widgets(self, user: User):
        """
        Disables the widgets of the form's fields depending on the user's permissions 
        so unauthorized users cannot enter data, yet still see the fields (in a disabled state).
        """
        # if user.has_perm("histopathological_sample.all_fields"):
        #     return
        
        # if user.has_perm("histopathological_sample.readonly"):
        #     for field in self.fields:
        #         self.fields[field].widget = forms.TextInput(attrs={"disabled": "true"})
        #     return
        
        print("Doing SOMETHING")

        if not user.has_perm("gui.recruiter_fields"):
            for field_name in recruiter_fields:
                self.disable_single_widget(field_name)
                self.disable_required_fields(field_name)

        if not user.has_perm("gui.tum_fields"):
            for field_name in tum_fields:
                self.disable_single_widget(field_name)

        if not user.has_perm("gui.spl_fields"):
            for field_name in spl_fields:
                print(field_name)
                self.disable_single_widget(field_name)

        if not user.has_perm("gui.sclab_fields"):
            for field_name in sclab_fields:
                self.disable_single_widget(field_name)

        if not user.has_perm("gui.spatial_fields"):
            for field_name in spatial_fields:
                self.disable_single_widget(field_name)

        if not user.has_perm("gui.lb_fields"):
            for field_name in lb_fields:
                self.disable_single_widget(field_name)

        if not user.has_perm("gui.omics_fields"):
            for field_name in odcf_fields:
                self.disable_single_widget(field_name)

    def disable_single_widget(self, field_name):
        # SAT3 Sample Code field is always enabled for users with write permissions.
        if not field_name == "saturn3_sample_code":
            self.fields[field_name].widget = forms.TextInput(attrs={"disabled": "true"})

    def disable_required_fields(self, field_name):
        """
        Required fields are necessary only when creating a new record
        i.e. if a user has the form's "recruiter_fields" set on enabled.
        If a user does not have these fields, then the fields must be set to not required
        in order to allow a form being submitted without said fields.
        """
        if not field_name == "saturn3_sample_code":
            if self.fields[field_name].required:
                self.fields[field_name].required = False


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
        } | date_pickers 


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

            "corresponding_organoid": forms.Select(
                attrs={"data-toggle": "tooltip",
                       "data-placement": "top",
                       "title": "generated from the same biopsy/tissue piece"},
                       ),

        } | disabled_tum_dict | disabled_spl_dict \
            | disabled_sclab_dict | disabled_spatial_dict \
            | disabled_lb_dict \
            | recruiter_date_pickers


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
            | disabled_spatial_dict | disabled_lb_dict \
            | tum_date_pickers


class SampleFormSPL(SampleFormTUM):
    """
    For SPL group members only

    The submission of this form can not create new records.
    """

    class Meta:
        model = HistopathologicalSample
        fields = all_field_names
        widgets = {

        } | disabled_sclab_dict \
            | disabled_spatial_dict | disabled_lb_dict \
            | spl_date_pickers


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
                        )

        } | disabled_tum_dict | disabled_spl_dict | disabled_lb_dict \
            | sclab_date_pickers


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
                        )

        } | disabled_tum_dict | disabled_spl_dict | disabled_lb_dict \
            | disabled_sclab_dict \
            | spatial_date_pickers


class SampleFormLB(SampleFormTUM):
    """
    For LB group members only

    The submission of this form can not create new records.
    """

    class Meta:
        model = HistopathologicalSample
        fields = all_field_names
        widgets = {

        } | disabled_tum_dict | disabled_spl_dict | disabled_sclab_dict \
            | disabled_spatial_dict \
            | lb_date_pickers


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

            "corresponding_organoid": forms.Select(
                attrs={"data-toggle": "tooltip",
                       "data-placement": "top",
                       "title": "generated from the same biopsy/tissue piece"},
                       )

        } | disabled_tum_dict | disabled_spl_dict \
            | disabled_sclab_dict | disabled_spatial_dict \
            | lb_date_pickers | recruiter_date_pickers
    


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
            | disabled_lb_dict \
            | odcf_date_pickers
        

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
