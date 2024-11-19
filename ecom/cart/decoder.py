from django.contrib.sessions.models import Session
key = '5t88hwlj71qtjdzqxzqxf0jbyaj5yhkc'
k = Session.objects.get(pk='5t88hwlj71qtjdzqxzqxf0jbyaj5yhkc')
k.get_decoded()

