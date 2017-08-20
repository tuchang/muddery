
"""
This contains a simple view for rendering the webclient
page and serve it eventual static content.

"""
from __future__ import print_function

import os, tempfile, time
from django.conf import settings
from django import http
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from evennia.utils import logger
from muddery.utils import utils
from muddery.utils.localized_strings_handler import _, LOCALIZED_STRINGS_HANDLER
from muddery.worlddata.data_sets import DATA_SETS
from muddery.utils.plugins_handler import PLUGINS_HANDLER


@staff_member_required
def plugins(request):
    """
    World Editor page template loading.
    """
    if "select_plugins" in request.POST:
        return select_plugins(request)

    return show_plugins(request)


@staff_member_required
def show_plugins(request):
    """
    Render a page of all plugins.

    Args:
        request:

    Returns:

    """
    plugins = []
    for key in os.listdir(settings.MUDDERY_PLUGINS_PATH):
        available = False
        loaded = PLUGINS_HANDLER.is_loaded(key)
        name = ""
        try:
            module_path = settings.MUDDERY_PLUGINS_DIR + "." + dir + ".handler"
            module = __import__(module_path, fromlist=["handler"])
            handler = module.HANDLER
            if handler:
                name = handler.name
                available = True
        except:
            pass

        plugins.append({"key": key,
                        "name": name,
                        "available":available,
                        "loaded": loaded})

    return render(request, 'plugins.html', {"plugins": plugins})


@staff_member_required
def select_plugins(request):
    """
    Select plugins.
    """
    response = http.HttpResponseNotModified()

    return response
