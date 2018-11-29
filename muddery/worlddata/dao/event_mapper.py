"""
Query and deal common tables.
"""

from __future__ import print_function

from evennia.utils import logger
from django.db import transaction
from django.apps import apps
from django.conf import settings
from muddery.utils import defines
from muddery.worlddata.dao.common_mapper_base import ObjectsMapper


class EventMapper(object):
    """
    Events data.
    """
    def __init__(self):
        self.model_name = "event_data"
        self.model = apps.get_model(settings.WORLD_DATA_APP, self.model_name)
        self.objects = self.model.objects

    def get_object_event(self, object_key):
        """
        Get an object's event.

        Args:
            object_key: (string) object's key.
        """
        return self.objects.filter(trigger_obj=object_key)

    def has_event(self, object_key):
        """
        If this object has events, returns True.

        Args:
            object_key: (string) object's key.
        """
        return self.objects.filter(trigger_obj=object_key).count() > 0

EVENTS = EventMapper()