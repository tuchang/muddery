"""
MudderyNPC is NPC's base class.

"""

import json
import traceback
from evennia import TICKER_HANDLER
from evennia.utils import logger
from muddery.typeclasses.characters import MudderyCharacter
from muddery.utils.localized_strings_handler import _
from muddery.utils.dialogue_handler import DIALOGUE_HANDLER
from muddery.utils.builder import build_object, delete_object
from muddery.utils.game_settings import GAME_SETTINGS
from muddery.worlddata.data_sets import DATA_SETS


class MudderyNPC(MudderyCharacter):
    """
    Default NPC. NPCs are friendly to players, they can not be attacked.
    """
    def at_object_creation(self):
        """
        Called once, when this object is first created. This is the
        normal hook to overload for most object types.
            
        """
        super(MudderyNPC, self).at_object_creation()

    def after_data_loaded(self):
        """
        Init the character.
        """
        super(MudderyNPC, self).after_data_loaded()

        # set home
        self.home = self.location

        # load dialogues.
        self.load_dialogues()

    def load_dialogues(self):
        """
        Load dialogues.
        """
        npc_key = self.get_data_key()
        dialogues = DATA_SETS.data("npc_dialogues").filter(npc=npc_key)

        self.default_dialogues = [dialogue.dialogue for dialogue in dialogues if dialogue.default]
        self.dialogues = [dialogue.dialogue for dialogue in dialogues if not dialogue.default]

    def get_available_commands(self, caller):
        """
        This returns a list of available commands.
        """
        commands = super(MudderyNPC, self).get_available_commands(caller)

        if self.dialogues or self.default_dialogues:
            # If the character have something to talk, add talk command.
            commands.append({"name":_("Talk"), "cmd":"talk", "args":self.dbref})

        return commands

    def have_quest(self, caller):
        """
        If the npc can complete or provide quests.
        Returns (can_provide_quest, can_complete_quest).
        """
        return DIALOGUE_HANDLER.have_quest(caller, self)
