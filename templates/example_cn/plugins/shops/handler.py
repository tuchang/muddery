"""
This model translates default strings into localized strings.
"""

from __future__ import print_function

import os
from django.conf import settings
from evennia.utils import logger
from evennia.commands.cmdsethandler import import_cmdset
from muddery.worlddata.data_sets import DATA_SETS
from muddery.worlddata.data_handler.file_data_handler import FileDataHandler
from muddery.utils.builder import build_object
from plugins.shops.commands import general


class Handler(object):
    """
    This model translates default strings into localized strings.
    """
    key = "shops"

    def at_init(self):
        """
        Called when init this plugin.
        """
        # Add data handler.
        group = ("file_data", "plugin", self.key,)
        DATA_SETS.add(FileDataHandler("typeclasses", self.key), group + ("typeclasses",))
        DATA_SETS.add(FileDataHandler("shops", self.key), group + ("object_data",))
        DATA_SETS.add(FileDataHandler("shop_goods", self.key), group + ("object_data",))
        DATA_SETS.add(FileDataHandler("npc_shops", self.key), group)
        
    def at_load_data(self):
        # load plugin data
        data_path = os.path.join(settings.MUDDERY_PLUGINS_PATH, self.key, "data")
        for data_handler in DATA_SETS.group(self.key):
            logger.log_info("Loading data " + data_handler.model_name())
            try:
                data_handler.import_from_path(data_path)
            except Exception, e:
                err_message = "Cannot import game data: %s" % e
                logger.log_tracemsg(err_message)

    def load_notifications(self, register):
        """
        Register notifications.
        """
        register.register_notification("CLASS_COMMON_NPC", "after_data_loaded", self)
        register.register_notification("CLASS_COMMON_NPC", "get_available_commands", self)
        
    def at_notification(self, typeclass, func_name, sender, args, kwargs, result):
        """
        """
        if func_name == "after_data_loaded":
            result = self.after_data_loaded(sender)
        elif func_name == "get_available_commands":
            result = self.get_available_commands(sender, result)

        return result
        
    def after_data_loaded(self, sender):
        # NPC's shop
        if not sender.attributes.has("shops"):
            sender.db.shops = {}

        # load shops
        self.load_shops(sender)

    def load_shops(self, sender):
        """
        Load sender's shop.
        """
        # shops records
        shop_records = DATA_SETS.data("npc_shops", self.key).filter(npc=sender.get_data_key())

        shop_keys = set([record.shop for record in shop_records])

        # remove old shops
        for shop_key in sender.db.shops:
            if shop_key not in shop_keys:
                # remove this shop
                sender.db.shops[shop_key].delete()
                del sender.db.shops[shop_key]

        # add new shop
        for shop_record in shop_records:
            shop_key = shop_record.shop
            if shop_key not in sender.db.shops:
                # Create shop object.
                shop_obj = build_object(shop_key, self.key)
                if not shop_obj:
                    logger.log_errmsg("Can't create shop: %s" % shop_key)
                    continue

                sender.db.shops[shop_key] = shop_obj

    def get_available_commands(self, sender, result):
        """
        Add shop's command to NPC.
        """
        commands = result
        if not commands:
            commands = []

        # Add shops.
        for shop_obj in sender.db.shops.values():
            if not shop_obj.is_visible(sender):
                continue

            verb = shop_obj.verb
            if not verb:
                verb = shop_obj.get_name()
            commands.append({"name":verb, "cmd":"shopping", "args":shop_obj.dbref})
            
        return commands
     
    def load_commands(self, cmdset):
        """
        Load plugin's commands.
        """
        key = cmdset.key
        if key == "DefaultCharacter":
            self.add_command(cmdset, general.CmdShopping())
            self.add_command(cmdset, general.CmdBuy())
                
    def add_command(self, cmdset, command):
        """
        """
        try:
            cmdset.add(command)
        except Exception, e:
            err_message = "Cannot add command: %s" % e
            logger.log_tracemsg(err_message)


# main plugin handler
HANDLER = Handler()
