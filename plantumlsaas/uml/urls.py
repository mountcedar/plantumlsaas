#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns
from django.conf.urls import url
from views import get


urlpatterns = patterns(
    '',
    url(r'^get', get, name='get'),
)
