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
        uml.image = os.path.join(STATIC_ROOT, uml.uuid.hex + ".png")
        query_string = "@startuml {%s}" % uml.image.name + os.linesep
        query_string += query + os.linesep
        query_string += "@enduml"

        fd, path = tempfile.mkstemp()
        fd.write(query_string)
        fd.close()

        # cmd = 'java -Djava.util.prefs.systemRoot=/javaw -Djava.util.prefs.userRoot=/javaw -Djava.awt.headless=true -jar /usr/local/lib/plantuml.jar '
        # cmd = 'java -Djava.awt.headless=true -Djava.util.prefs.systemRoot=/javaw -jar /usr/local/lib/plantuml.jar'
        cmd = 'java -Djava.util.prefs.systemRoot=/javaw -Djava.awt.headless=true -jar /usr/local/lib/plantuml.jar '
        p = subprocess.Popen(
            cmd + path,
            shell=True,
            # stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        # p.wait()
        # p.stdin.write(query_string)
        out, err = p.communicate()

        os.remove(temp.name)

        with uml.image.open() as f:
            uml.image_url = os.path.join(STATIC_URL, uml.uuid.hex + ".png")
            uml.save()
            return HttpResponse(f.read(), content_type="image/png")
    except:
        return HttpResponse(
            traceback.format_exc(),# + os.linesep + out + os.linesep + err + os.linesep,
            content_type="text/plain"
        )
