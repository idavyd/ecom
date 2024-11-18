from django.contrib.sessions.models import Session
key = 'ci4p4zx0seiyg5ixgmxbe53gultr0yhj'
k = Session.objects.get(pk='ci4p4zx0seiyg5ixgmxbe53gultr0yhj')
k.get_decoded()

