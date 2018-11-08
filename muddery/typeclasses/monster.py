"""
MudderyMob is mob's base class.

"""

import json
import traceback
from django.conf import settings
from evennia.utils import logger
from muddery.utils.builder import delete_object
from muddery.utils.localized_strings_handler import _
from muddery.utils.game_settings import GAME_SETTINGS
from muddery.worlddata.dao.npc_dialogues_mapper import NPC_DIALOGUES
from muddery.mappings.typeclass_set import TYPECLASS


class MudderyMonster(TYPECLASS("WORLD_CHARACTER")):
    """
    Default mob. Monsters are hostile to players, they can be attacked.
    """
    typeclass_key = "MONSTER"
    typeclass_name = _("Monster", "typeclasses")
    __all_models__ = None

    def after_data_loaded(self):
        """
        Init the character.
        """
        super(MudderyMonster, self).after_data_loaded()
        
        # Character can auto fight.
        self.auto_fight = True
        
        # set home
        self.home = self.location
        
        # load dialogues.
        self.load_dialogues()

    def load_dialogues(self):
        """
        Load dialogues.
        """
        dialogues = NPC_DIALOGUES.filter(self.get_data_key())

        self.default_dialogues = [dialogue.dialogue for dialogue in dialogues if dialogue.default]
        self.dialogues = [dialogue.dialogue for dialogue in dialogues if not dialogue.default]

    def get_available_commands(self, caller):
        """
        This returns a list of available commands.
        """
        commands = []
        if self.is_alive():
            if self.dialogues or self.default_dialogues:
                # If the character have something to talk, add talk command.
                commands.append({"name":_("Talk"), "cmd":"talk", "args":self.dbref})
            
            commands.append({"name": _("Attack"), "cmd": "attack", "args": self.dbref})
        return commands

