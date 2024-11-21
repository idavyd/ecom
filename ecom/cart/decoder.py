from django.contrib.sessions.models import Session
key = '04yg6zx4rt88sy96op5g0gu4x9ybw02w'
k = Session.objects.get(pk='04yg6zx4rt88sy96op5g0gu4x9ybw02w')
k.get_decoded()

