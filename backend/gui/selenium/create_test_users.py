from django.contrib.auth.models import User

user = User.objects.create_user('root', password='root')
user.is_superuser = True
user.is_staff = True
user.save()
