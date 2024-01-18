from django.contrib.auth.models import User, Group

recruiter_group, created = Group.objects.get_or_create(name='Recruiter')
spl_group, created = Group.objects.get_or_create(name='SPL')
sclab_group, created = Group.objects.get_or_create(name='ScLab')
lb_group, created = Group.objects.get_or_create(name='LB')
tum_group, created = Group.objects.get_or_create(name='TUM')


berto = User.objects.create_user("berto", "", "bertobeschde")

berto_recruiter = User.objects.create_user(
    "berto_Recruiter", "", "bertobeschde")
berto_recruiter.save()
berto_recruiter.groups.add(recruiter_group)

berto_spl = User.objects.create_user("berto_SPL", "", "bertobeschde")
berto_spl.save()
berto_spl.groups.add(spl_group)

berto_sclab = User.objects.create_user("berto_scLab", "", "bertobeschde")
berto_sclab.save()
berto_sclab.groups.add(sclab_group)

berto_lb = User.objects.create_user("berto_LB", "", "bertobeschde")
berto_lb.save()
berto_lb.groups.add(lb_group)

berto_tum = User.objects.create_user("berto_TUM", "", "bertobeschde")
berto_tum.save()
berto_tum.groups.add(tum_group)
