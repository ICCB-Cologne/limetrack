from django.contrib.auth.models import User, Group

user = User.objects.create_user('root', password='root')
user.is_superuser = True
user.is_staff = True
user.save()

user2 = User.objects.create_user('test_SPL', password='test4life')
user2.save()
my_group = Group.objects.get(name='SPL')
my_group.user_set.add(user2)
