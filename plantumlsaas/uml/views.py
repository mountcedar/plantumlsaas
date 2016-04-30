from django.shortcuts import render

# Create your views here.

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import traceback
import logging
import subprocess
import tempfile
import urllib

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
        if created:
            uml.image = os.path.join(STATIC_ROOT, uml.uuid.hex + ".png")
            query_string = "@startuml{%s}" % (uml.uuid.hex + ".png") + os.linesep
            query_string += urllib.unquote(query).replace(';', os.linesep) + os.linesep
            query_string += "@enduml"

            fd, path = tempfile.mkstemp()
            os.close(fd)
            with open(path, 'w') as fp:
                fp.write(query_string)

            cmd = 'java -Djava.util.prefs.systemRoot=/javaw -Djava.awt.headless=true -jar /usr/local/lib/plantuml.jar '
            p = subprocess.Popen(
                cmd + path,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            out, err = p.communicate()
            if err:
                return HttpResponse(out, state=500, content_type="text_plain")

            os.remove(path)
            os.rename(
                os.path.join(os.path.dirname(path), uml.uuid.hex + ".png"),
                os.path.join(STATIC_ROOT, uml.uuid.hex + ".png")
            )
            uml.image_url = os.path.join(STATIC_URL, uml.uuid.hex + ".png")
            uml.save()

        with open(os.path.join(STATIC_ROOT, uml.uuid.hex + ".png"), 'rb') as fp:
            return HttpResponse(fp.read(), content_type="image/png")
    except:
        return HttpResponse(
            traceback.format_exc(),
            content_type="text/plain"
        )
