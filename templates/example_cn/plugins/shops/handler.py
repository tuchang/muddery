"""
This model translates default strings into localized strings.
"""

from __future__ import print_function

import os
from django.conf import settings
from evennia.utils import logger
from muddery.worlddata.data_sets import DATA_SETS
from muddery.worlddata.data_handler.file_data_handler import FileDataHandler


class Handler(object):
    """
    This model translates default strings into localized strings.
    """
    name = "shops"

    def at_init(self):
        """
        Called when init this plugin.
        """
        # Add data handler.
        group = ("file_data", "plugin", self.name,)
        DATA_SETS.add(FileDataHandler("typeclasses", self.name), group + ("typeclasses",))
        DATA_SETS.add(FileDataHandler("shops", self.name), group)
        DATA_SETS.add(FileDataHandler("shop_goods", self.name), group)
        DATA_SETS.add(FileDataHandler("npc_shops", self.name), group)
        
    def at_load_data(self):
        # load plugin data
        data_path = os.path.join(settings.MUDDERY_PLUGINS_PATH, self.name, "data")
        for data_handler in DATA_SETS.group(self.name):
            logger.log_info("Loading data " + data_handler.model_name())
            try:
                data_handler.import_from_path(data_path)
            except Exception, e:
                err_message = "Cannot import game data. %s" % e
                logger.log_tracemsg(err_message)
        

# main plugin handler
HANDLER = Handler()
