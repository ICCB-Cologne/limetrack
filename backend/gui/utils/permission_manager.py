from ..forms.forms import field_dict
from django.contrib.auth.models import User

def get_all_permitted_fields(user: User):
        
        permitted_fields = []
        print("user.get_user_permissions")
        for permission in user.get_all_permissions():
            print("permission")
            if not "_fields" in permission:
                  continue
            # e.g. gui.recruiter_fields -> recruiter
            model_section = permission.split("_")[0].split(".")[1]
            print("model_section")
            print(model_section)
            permitted_fields += field_dict[model_section]

        print("permitted_fields")
        print(permitted_fields)
        return permitted_fields
