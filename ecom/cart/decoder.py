from django.contrib.sessions.models import Session
key = 't2y8or7eout1znrd9yci1jkn4v47tm1m'
k = Session.objects.get(pk='t2y8or7eout1znrd9yci1jkn4v47tm1m')
k.get_decoded()

