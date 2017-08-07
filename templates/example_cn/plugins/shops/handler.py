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

    def at_load_notifications(self, register):
        """
        Register notifications.
        """
        register.register_notification("CLASS_COMMON_NPC", "after_data_loaded", self)
        
    def at_notification(self, typeclass, func_name, caller, args, kwargs, result):
        """
        """
        print("typeclass: %s" % typeclass)
        print("func_name: %s" % func_name)
        print("caller: %s" % caller)
        print("args: %s" % (args,))
        print("kwargs: %s" % kwargs)
        print("result: %s" % (result,))
        
        if func_name == "after_data_loaded":
            self.after_data_loaded(caller)

        return result
        
    def after_data_loaded(self, caller):
        # NPC's shop
        if not caller.attributes.has("shops"):
            caller.db.shops = {}

        # load shops
        self.load_shops(caller)

    def load_shops(self, caller):
        """
        Load caller's shop.
        """
        # shops records
        shop_records = DATA_SETS.data("npc_shops").filter(npc=caller.get_data_key())

        shop_keys = set([record.shop for record in shop_records])

        # remove old shops
        for shop_key in caller.db.shops:
            if shop_key not in shop_keys:
                # remove this shop
                caller.db.shops[shop_key].delete()
                del caller.db.shops[shop_key]

        # add new shop
        for shop_record in shop_records:
            shop_key = shop_record.shop
            if shop_key not in caller.db.shops:
                # Create shop object.
                shop_obj = build_object(shop_key)
                if not shop_obj:
                    logger.log_errmsg("Can't create shop: %s" % shop_key)
                    continue

                caller.db.shops[shop_key] = shop_obj

# main plugin handler
HANDLER = Handler()
