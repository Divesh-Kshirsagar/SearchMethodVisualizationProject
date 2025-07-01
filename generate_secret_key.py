#!/usr/bin/env python
"""
Django SECRET_KEY generator.
"""
from django.core.management.utils import get_random_secret_key

print(get_random_secret_key())
