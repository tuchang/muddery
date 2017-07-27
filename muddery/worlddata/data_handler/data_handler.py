"""
This module defines available model types.
"""
import os
import glob
import traceback
from django.apps import apps
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from evennia.utils import logger
from muddery.utils import readers
from muddery.utils.exception import MudderyError


class DataHandler(object):
    """

    """
    def __init__(self, model_name):
        """

        Args:
            model_name:

        Returns:

        """
        self._model_name = model_name
        self._model = None
        self._objects = None
        
        try:
            self._model = apps.get_model(settings.WORLD_DATA_APP, self._model_name)
            self._objects = self._model.objects
        except Exception, e:
            ostring = "Can not load model %s: %s" % (self._model_name, e)
            print(ostring)
            logger.log_errmsg(ostring)

    def model_name(self):
        """
        Get model's name.

        Returns:
            model's name
        """
        return self._model_name

    def clear_model_data(self, **kwargs):
        """
        Remove all data from db.

        Args:
            model_name: (string) db model's name.

        Returns:
            None
        """
        # clear old data
        self._objects.all().delete()

    def all(self):
        """
        Get all records.

        Returns:
            query result
        """
        return self._objects.all()

    def filter(self, *args, **kwargs):
        """
        Query records.

        Returns:
            query result
        """
        return self._objects.filter(*args, **kwargs)

    def get(self, *args, **kwargs):
        """
        Query records.

        Returns:
            query result
        """
        return self._objects.get(*args, **kwargs)
