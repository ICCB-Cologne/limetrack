from ..models import HistopathologicalSample, end_of_model_section_dict
from ..utils.fields import SampleCodeField, SampleCodeWidget
from ..utils import model_to_form
from tempus_dominus.widgets import DatePicker  # type: ignore
from django.forms import ModelForm
from django import forms

# documentation on DatePickers
# https://github.com/FlipperPA/django-tempus-dominus


# all displayed fields' names and verbose_names
all_field_verbose_names = []
all_field_names = []

# date_picker widgets for the form
date_pickers = {}

# exclude primary key "ID" & "created" field by slicing
# for we dont want them displayed or edited
all_fields = HistopathologicalSample._meta.get_fields()[1:-1]

for field in all_fields:
    all_field_verbose_names.append(field.verbose_name)
    all_field_names.append(field.name)
    # creation of DatePicker widgets for each DateField
    if field.get_internal_type() == "DateField":
        date_pickers.update(
            {
                field.name: DatePicker(
                    options={"allowInputToggle": True},
                    attrs={"input_group": False})
            })


# create dictionary with lists of fields for the
# individual groups or data model sections
field_dict = model_to_form.create_field_dict(
    model_section_dict=end_of_model_section_dict,
    all_fields=all_fields,
    all_field_names=all_field_names)


class FlexibleSampleForm(ModelForm):
    """
    This form disables fields depending on the permissions a user has.

    """
    required_css_class = "required"
    # error_css_class = "error-field"

    saturn3_sample_code = SampleCodeField(
        required=True, widget=SampleCodeWidget(), label="SATURN3 Sample Code")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        model_to_form.adapt_form(self, user, field_dict)

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
                attrs={'min': 0, 'max': 5, 'type': 'number'}
            ),
        } | date_pickers


def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.xlsx', '.csv', '.xls']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


class UploadForm(forms.Form):
    file = forms.FileField(help_text="Upload '.csv' or '.xlsx' files.",
                           allow_empty_file=False,
                           validators=[validate_file_extension])


class GroupFilterForm(forms.Form):
    """
    Enables filtering of the sample tables's columns by section and/or
    customly defined sets of data fields.
    The actual filtering is handled in samples_view.py
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

    scrnaseq = forms.BooleanField(initial=True,
                                  required=False,
                                  label="ScRNASeq")

    wgs = forms.BooleanField(initial=True,
                             required=False,
                             label="WGS")

    variantcalling = forms.BooleanField(initial=True,
                                        required=False,
                                        label="Variant Calling")


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
