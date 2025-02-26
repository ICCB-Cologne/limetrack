from ..forms.forms import field_dict
from django.contrib.auth.models import User


def get_all_permitted_fields(user: User):
    """
    Returns a list of all field names of the sections
    a user is permitted to fill.
    """
    permitted_fields = []
    for permission in user.get_all_permissions():
        # exclude permissions that have nothing to do with models sections
        if "_fields" not in permission:
            continue
        # e.g. gui.recruiter_fields -> recruiter
        model_section = permission.split("_")[0].split(".")[1]
        permitted_fields += field_dict[model_section]

    return permitted_fields
