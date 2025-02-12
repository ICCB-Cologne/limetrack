from tempus_dominus.widgets import DatePicker
from django.db.models.fields import Field
from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms



def create_date_picker_dicts(date_pickers: dict[str: DatePicker], field_dict):

    recruiter_date_pickers = {field_name : date_pickers.get(field_name)
                            for field_name in date_pickers if field_name in field_dict["recruiter"]}

    tum_date_pickers = {field_name : date_pickers.get(field_name)
                            for field_name in date_pickers if field_name in field_dict["tum"]}

    spl_date_pickers = {field_name : date_pickers.get(field_name)
                            for field_name in date_pickers if field_name in field_dict["spl"]}

    sclab_date_pickers = {field_name : date_pickers.get(field_name)
                            for field_name in date_pickers if field_name in field_dict["scopenlab"]}

    spatial_date_pickers = {field_name : date_pickers.get(field_name)
                            for field_name in date_pickers if field_name in field_dict["spatial"]}

    lb_date_pickers = {field_name : date_pickers.get(field_name)
                            for field_name in date_pickers if field_name in field_dict["liquidbiopsy"]}

    odcf_date_pickers = {field_name : date_pickers.get(field_name)
                            for field_name in date_pickers if field_name in field_dict["omicspath"]}
    
    return recruiter_date_pickers, tum_date_pickers, \
           spl_date_pickers, sclab_date_pickers, \
           spatial_date_pickers, \
           lb_date_pickers, odcf_date_pickers


def fill_form_collections(all_fields, all_field_verbose_names, date_pickers, all_field_names):
    """
    TODO: exchange a call of this function with the code block in forms.py
    """
    
    for field in all_fields:
        all_field_verbose_names.append(field.verbose_name)
        all_field_names.append(field.name)
        if field.get_internal_type() == "DateField":
            date_pickers.update(
                {field.name : DatePicker(
                    options={"allowInputToggle": True},
                    attrs={"input_group": False})
                    })




def create_field_dict(model_section_dict,
                      all_fields: list[Field],
                      all_field_names: list[str]) -> dict[str: list[str]]:
    """
    We need a dict that contains the names of all sections (keys) and
    their respective field names (values).
    This allows us to always check which permissions allow writing to which fields.
    
    returns:
    { "recruiter" : ["recruiting_site", "sex", ...],
      "tum" : [...],
      ...
    }
    
    """

    field_dict = {}
    start_index = 0
    for section in model_section_dict:
        section_end = model_section_dict[section]
        end_index = all_field_names.index(section_end)
        section_fields = all_field_names[start_index:end_index+1]
        field_dict.update({section   : section_fields})
        start_index = end_index + 1
    
    print(field_dict)
    return field_dict


def adapt_form(form: ModelForm, user: User, field_dict: dict):
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
    # TODO: generalize this!
    if not user.has_perm("gui.recruiter_fields"):
        for field_name in field_dict["recruiter"]:
            disable_single_widget(form, field_name)
            disable_required_fields(form, field_name)

    if not user.has_perm("gui.tum_fields"):
        for field_name in field_dict["tum"]:
            disable_single_widget(form, field_name)

    if not user.has_perm("gui.spl_fields"):
        for field_name in field_dict["spl"]:
            disable_single_widget(form, field_name)

    if not user.has_perm("gui.scopenlab_fields"):
        for field_name in field_dict["scopenlab"]:
            disable_single_widget(form, field_name)

    if not user.has_perm("gui.spatial_fields"):
        for field_name in field_dict["spatial"]:
            disable_single_widget(form, field_name)

    if not user.has_perm("gui.liquidbiopsy_fields"):
        for field_name in field_dict["liquidbiopsy"]:
            disable_single_widget(form, field_name)

    if not user.has_perm("gui.omicspath_fields"):
        for field_name in field_dict["omicspath"]:
            disable_single_widget(form, field_name)
            # TODO: generalize this if necessary
            # In our form we do not 
            # want to visualize the odcf fields
            # for not-odcf-users
            if not field_name == "saturn3_sample_code":
                form.fields.pop(field_name)

def disable_single_widget(form: ModelForm, field_name):
    # SAT3 Sample Code field is always enabled for users with write permissions.
    if not field_name == "saturn3_sample_code":
        form.fields[field_name].widget = forms.TextInput(attrs={"disabled": "true"})

def disable_required_fields(form: ModelForm, field_name):
    """
    Required fields are necessary only when creating a new record
    i.e. if a user has the form's "recruiter_fields" set on enabled.
    If a user does not have these fields, then the fields must be set to not required
    in order to allow a form being submitted without said fields.
    """
    if not field_name == "saturn3_sample_code":
        if form.fields[field_name].required:
            form.fields[field_name].required = False
