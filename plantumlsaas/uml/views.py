from django.shortcuts import render

# Create your views here.

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import traceback
import logging
import subprocess

import requests
from PIL import Image

from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
# from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from models import UML
from plantumlsaas.settings import STATIC_URL
from plantumlsaas.settings import STATIC_ROOT


@csrf_exempt
def get(request):
    try:
        if request.method != "GET":
            raise Http404
        query = request.META['QUERY_STRING']

        uml, created = UML.objects.get_or_create(query=query)
        x = os.path.join(STATIC_ROOT, uml.uuid.hex + ".png")
        query_string = "@startuml {%s}" % uml.image + os.linesep
        query_string += query
        query_string += "@enduml"

        cmd = 'java -jar /usr/local/lib/plantuml.jar'
        p = subprocess.Popen(
            cmd,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            # stderr=subprocess.PIPE
        )
        # p.wait()
        p.stdin.write(query_string)
        p.communicate()

        with open(uml.image.filename, "rb") as f:
            uml.image_url = os.path.join(STATIC_URL, uml.uuid.hex + ".png")
            uml.save()
            return HttpResponse(f.read(), content_type="image/png")
    except IOError, ioe:
        return HttpResponse(traceback.format_exc(), content_type="text/plain")
    except OSError, ose:
        return HttpResponse(traceback.format_exc(), content_type="text/plain")
    except Exception, e:
        return HttpResponse(traceback.format_exc(), content_type="text/plain")
