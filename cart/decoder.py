from django.contrib.sessions.models import Session
key = 'wjpbywzcckz69cr6sc5npi9qqks8d3ho'
k = Session.objects.get(pk='wjpbywzcckz69cr6sc5npi9qqks8d3ho')
k.get_decoded()

