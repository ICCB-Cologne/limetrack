"""
Only important for github actions in order to create users, groups & permissions inside the docker container
Has to be adapted for other models & user management
"""
from django.contrib.auth.models import User, Group
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

groups_and_their_permissions = {
    "SPL" : ["spl_fields"],
    "Recruiter" : ["recruiter_fields"],
    "LiquidBiopsy" : ["liquidbiopsy_fields"],
    "scOpenLab" : ["scopenlab_fields"],
    "OmicsPath" : ["omicspath_fields"],
    "TUM" : ["tum_fields"],
    "Spatial" : ["spatial_fields"],
}

# here we create one user for each group and each group has only permissions for their original section in the model 
ct = ContentType.objects.get(app_label="gui", model='histopathologicalsample',)

for group in groups_and_their_permissions:
    user = User.objects.create_user(f'test_{group}', password='test4life')
    new_group, created = Group.objects.get_or_create(name=group)
    new_group.user_set.add(user)
    for permission in groups_and_their_permissions[group]:
        new_permission = Permission.objects.get_or_create(name=permission, codename=f"codename_{permission}", content_type=ct)
        print("we here")
        new_group.permissions.add(new_permission)
        print("we not here")
    new_group.save()
    user.save()