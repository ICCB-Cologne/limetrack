from django.contrib.auth.models import User, Group

user = User.objects.create_user('test_SPL', password='test4life')
user.save()
new_group, created = Group.objects.get_or_create(name='SPL')
new_group.user_set.add(user)
