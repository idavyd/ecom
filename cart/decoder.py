from django.contrib.sessions.models import Session
key = '2vl3dorl4aiczt3lkibvfogj1219j3k3'
k = Session.objects.get(pk='2vl3dorl4aiczt3lkibvfogj1219j3k3')
k.get_decoded()

