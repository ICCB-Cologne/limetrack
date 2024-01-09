from django import forms
from django.forms import ModelForm
from .models import HistopathologicalSample
from .widgets import BootstrapDateTimePickerInput
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker

# MODEL_CHOICES = [
#     ('ViT', 'ViT'),
#     ('ResNet-50', 'ResNet-50'),
# ]
# DR_METHODS = [
#     ('HNNE', 'HNNE'),
#     ('T-SNE', 'T-SNE'),
#     ('MDS', 'MDS'),
#     ('PCA', 'PCA'),
#     ('ISOMAP', 'ISOMAP'),
#
# ]
# DIMENSIONS = [
#     (3, 3),
#     (2, 2),
# ]
#
#
# # SHAPE_ADJUSTMENT_METHOD = [
# #     ('None', 'None (assumes 1024 x 1024 RGB)'),
# #     ('Resize', 'Resize'),
# #     ('Pad', 'Pad'),
# # ]
#
# class MultipleFileInput(forms.ClearableFileInput):
#     allow_multiple_selected = True
#
#
# class MultipleFileField(forms.FileField):
#     def __init__(self, *args, **kwargs):
#         kwargs.setdefault("widget", MultipleFileInput())
#         super().__init__(*args, **kwargs)
#
#     def clean(self, data, initial=None):
#         single_file_clean = super().clean
#         if isinstance(data, (list, tuple)):
#             result = [single_file_clean(d, initial) for d in data]
#         else:
#             result = single_file_clean(data, initial)
#         return result
#
#
# class ConfigurationForm(forms.Form):
#     project_name = forms.CharField(
#         max_length=50,
#         widget=forms.TextInput(attrs={'class': 'form-control'}),
#         label='Project Recruiting_site',
#         required=True
#     )
#
#     input_path = MultipleFileField(
#         required=False,
#         label='Add / upload files to project',
#     )
#
#     model = forms.ChoiceField(
#         choices=MODEL_CHOICES,
#         widget=forms.Select(attrs={'class': 'form-control'}),
#         label='Model'
#     )
#
#     dr_method = forms.ChoiceField(
#         choices=DR_METHODS,
#         widget=forms.Select(attrs={'class': 'form-control'}),
#         label='Dimensionality reduction method'
#     )
#
#     desired_dims = forms.ChoiceField(
#         choices=DIMENSIONS,
#         widget=forms.Select(attrs={'class': 'form-control'}),
#         label='Output dimensions'
#     )


class SampleForm(ModelForm):
    # died = forms.DateField(widget=DatePicker())
    required_css_class = "required"
    error_css_class = "error-field"

    class Meta:
        model = HistopathologicalSample
        # fields must be replaced in production by a list of all fields due to security reasons
        fields = "__all__"
        widgets = {
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
            'died': DatePicker(options={}, attrs={"input_group": False}),
            'sampling_date': DatePicker(options={}, attrs={"input_group": False}),
            'spl_received': DatePicker(options={}, attrs={"input_group": False}),
            'sclab_received': DatePicker(options={}, attrs={"input_group": False}),
            'sclab_extraction_date': DatePicker(options={}, attrs={"input_group": False}),
            'lb_sampling_date': DatePicker(options={}, attrs={"input_group": False}),
            'lb_received': DatePicker(options={}, attrs={"input_group": False}),
            'lb_date_of_isolation': DatePicker(options={}, attrs={"input_group": False})
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
    password = forms.CharField()
