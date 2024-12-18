from tempus_dominus.widgets import DatePicker

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