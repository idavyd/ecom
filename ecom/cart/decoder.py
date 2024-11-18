from django.contrib.sessions.models import Session


key = 'ipaklwu0lhhvf51ctdmqda2qsha93sz8'
k = Session.objects.get(pk='ipaklwu0lhhvf51ctdmqda2qsha93sz8')
k.get_decoded()

