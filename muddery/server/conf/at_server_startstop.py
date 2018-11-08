"""
Server startstop hooks

This module contains functions called by Evennia at various
points during its startup, reload and shutdown sequence. It
allows for customizing the server operation as desired.

This module must contain at least these global functions:

at_server_start()
at_server_stop()
at_server_reload_start()
at_server_reload_stop()
at_server_cold_start()
at_server_cold_stop()

"""

from muddery.utils.attributes_info_handler import CHARACTER_ATTRIBUTES_INFO, EQUIPMENT_ATTRIBUTES_INFO, FOOD_ATTRIBUTES_INFO
from muddery.utils.dialogue_handler import DIALOGUE_HANDLER
from muddery.utils.equip_type_handler import EQUIP_TYPE_HANDLER
from muddery.utils.localized_strings_handler import LOCALIZED_STRINGS_HANDLER
from muddery.utils.game_settings import GAME_SETTINGS
from muddery.utils.desc_handler import DESC_HANDLER
from muddery.dao.honours_mapper import HONOURS_MAPPER
from muddery.utils import builder
from muddery.utils.localiztion_handler import localize_model_fields

def at_server_start():
    """
    This is called every time the server starts up, regardless of
    how it was shut down.
    """
    # reset settings
    GAME_SETTINGS.reset()

    # reload local strings
    LOCALIZED_STRINGS_HANDLER.reload()

    # reload attributes
    CHARACTER_ATTRIBUTES_INFO.reload()
    EQUIPMENT_ATTRIBUTES_INFO.reload()
    FOOD_ATTRIBUTES_INFO.reload()

    # reset default locations
    builder.reset_default_locations()
    
    # clear dialogues
    DIALOGUE_HANDLER.clear()
    
    # reload equipment types
    EQUIP_TYPE_HANDLER.reload()

    # localize model fields
    localize_model_fields()

    # set character attribute field names
    CHARACTER_ATTRIBUTES_INFO.set_model_fields()
    EQUIPMENT_ATTRIBUTES_INFO.set_model_fields()
    FOOD_ATTRIBUTES_INFO.set_model_fields()
    
    # load condition descriptions
    DESC_HANDLER.reload()
    
    # load honours    
    HONOURS_MAPPER.reload()

def at_server_stop():
    """
    This is called just before the server is shut down, regardless
    of it is for a reload, reset or shutdown.
    """
    pass


def at_server_reload_start():
    """
    This is called only when server starts back up after a reload.
    """
    pass


def at_server_reload_stop():
    """
    This is called only time the server stops before a reload.
    """
    pass


def at_server_cold_start():
    """
    This is called only when the server starts "cold", i.e. after a
    shutdown or a reset.
    """
    pass


def at_server_cold_stop():
    """
    This is called only when the server goes down due to a shutdown or
    reset.
    """
    pass
