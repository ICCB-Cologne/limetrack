from ..forms.forms import field_dict
from django.contrib.auth.models import User

def get_all_permitted_fields(user: User):
        
        permitted_fields = []
        for permission in user.get_user_permissions():
            model_section = permission.split("_")[0]
            permitted_fields.append(field_dict[model_section])

        return permitted_fields
