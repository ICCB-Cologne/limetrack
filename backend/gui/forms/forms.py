from ..models import HistopathologicalSample, CHARFIELD_MAXLEN, end_of_model_section_dict
from ..utils.fields import SampleCodeField, SampleCodeWidget
from ..utils.model_choices import (
                     SITE_CHOICES, SEX_CHOICES,
                     TISSUE_TYPES, INTERVENTION_TYPES,
                     GRADING,
                     CORRESPONDING_ORGANOID_CHOICES,
                     LOCALISATION_CHOICE)
from ..utils.model_to_form import(
    create_date_picker_dicts, create_field_dict
)
from tempus_dominus.widgets import DatePicker #type: ignore
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
# documentation https://github.com/FlipperPA/django-tempus-dominus


all_field_verbose_names = []
all_field_names = []
date_pickers = {}

# exclude primary key "ID" & field "created" by slicing
# for we dont want them displayed or edited
all_fields = HistopathologicalSample._meta.get_fields()[1:-1]

for field in all_fields:
    all_field_verbose_names.append(field.verbose_name)
    all_field_names.append(field.name)
    # creation of DatePicker widgets for each DateField 
    if field.get_internal_type() == "DateField":
        date_pickers.update(
            {field.name : DatePicker(
                options={"allowInputToggle": True},
                attrs={"input_group": False})
                })
    


# lists of fields for individual groups
# TODO: after adding new model fields
# if necessary
# change indexes here by changing the first
# and the last model field name of a group

field_dict = create_field_dict(model_section_dict=end_of_model_section_dict,
                  all_fields=all_fields,
                  all_field_names=all_field_names)

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
        
        if not user.has_perm("gui.recruiter_fields"):
            for field_name in field_dict["recruiter"]:
                self.disable_single_widget(field_name)
                self.disable_required_fields(field_name)

        if not user.has_perm("gui.tum_fields"):
            for field_name in field_dict["tum"]:
                self.disable_single_widget(field_name)

        if not user.has_perm("gui.spl_fields"):
            for field_name in field_dict["spl"]:
                self.disable_single_widget(field_name)

        if not user.has_perm("gui.scopenlab_fields"):
            for field_name in field_dict["scopenlab"]:
                self.disable_single_widget(field_name)

        if not user.has_perm("gui.spatial_fields"):
            for field_name in field_dict["spatial"]:
                self.disable_single_widget(field_name)

        if not user.has_perm("gui.liquidbiopsy_fields"):
            for field_name in field_dict["liquidbiopsy"]:
                self.disable_single_widget(field_name)

        if not user.has_perm("gui.omicspath_fields"):
            for field_name in field_dict["omicspath"]:
                self.disable_single_widget(field_name)
                # TODO: generalize this if necessary
                # In our form we do not 
                # want to visualize the odcf fields
                # for not-odcf-users
                if not field_name == "saturn3_sample_code":
                    self.fields.pop(field_name)

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
        fields = all_field_names


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
