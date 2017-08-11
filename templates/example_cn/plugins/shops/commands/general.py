"""
General Character commands usually availabe to all characters

This is adapt from evennia/evennia/commands/default/general.py.
The licence of Evennia can be found in evennia/LICENSE.txt.
"""

from django.conf import settings
from evennia.utils import logger
from evennia.commands.command import Command
from muddery.utils.localized_strings_handler import _


#------------------------------------------------------------
# open a shop
#------------------------------------------------------------
class CmdShopping(Command):
    """
    Open a shop.

    Usage:
        {"cmd":"shopping",
         "args":<shop's dbref>
        }
    """
    key = "shopping"
    locks = "cmd:all()"
    help_cateogory = "General"

    def func(self):
        "Do shopping."
        caller = self.caller

        if not self.args:
            caller.msg({"alert":_("You should shopping in someplace.")})
            return

        shop = caller.search(self.args)
        if not shop:
            caller.msg({"alert":_("Can not find this shop.")})
            return

        shop.show_shop(caller)


#------------------------------------------------------------
# buy goods
#------------------------------------------------------------
class CmdBuy(Command):
    """
    Buy goods.

    Usage:
        {"cmd":"buy",
         "args":<goods' dbref>}
        }
    """
    key = "buy"
    locks = "cmd:all()"
    help_cateogory = "General"

    def func(self):
        "Buy a goods."
        caller = self.caller

        if not self.args:
            caller.msg({"alert":_("You should buy something.")})
            return

        goods = caller.search(self.args)
        if not goods:
            caller.msg({"alert":_("Can not find this goods.")})
            return

        # buy goods
        try:
            goods.sell_to(caller)
        except Exception, e:
            caller.msg({"alert":_("Can not buy this goods.")})
            logger.log_err("Can not buy %s: %s" % (goods.get_data_key(), e))
            return
