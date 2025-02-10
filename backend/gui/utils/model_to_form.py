from tempus_dominus.widgets import DatePicker
from django.db.models.fields import Field

@staticmethod
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