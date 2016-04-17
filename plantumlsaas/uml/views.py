from django.shortcuts import render

# Create your views here.

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render

import os
import urllib
import urllib2
import json
import traceback
import logging

import requests
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
# from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.http import urlencode
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from django.core import serializers

@csrf_exempt
def get(request):
    if request.method != "GET":
        raise Http404
    query = request.QUERY_STRING

    return HttpResponse(json.dumps({'str': query}), 'json/application')
