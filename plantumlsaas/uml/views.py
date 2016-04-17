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

@csrf_exempt
def get(request):
    try:
        if request.method != "GET":
            raise Http404
        query = request.META['QUERY_STRING']
        cmd = 'java -jar /usr/local/lib/plantuml.jar'
        p = subprocess.Popen(
            cmd,
            # shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        p.wait()
        p.stdin.write(query)
        p.communicate()
        with open('image.png', "rb") as f:
            return HttpResponse(f.read(), content_type="image/png")
    except IOError:
        red = Image.new('RGBA', (1, 1), (255,0,0,0))
        response = HttpResponse(content_type="image/jpeg")
        red.save(response, "JPEG")
        return response
