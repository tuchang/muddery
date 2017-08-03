"""
This module defines available model types.
"""

from django.conf import settings
from evennia.utils.utils import class_from_module
from muddery.worlddata.data_handler.data_handler import DataHandler
from muddery.worlddata.data_handler.file_data_handler import FileDataHandler
from muddery.worlddata.data_handler.system_data_handler import SystemDataHandler
from muddery.worlddata.data_handler.localized_strings_handler import LocalizedStringsHandler


class DataSets(object):

    def __init__(self):
        """
        Load data settings.

        Returns:
            None.
        """
        # initial containers
        self._handler_dict = {}
        self._groups = {}
        
        # load world data
        self.load_worlddata()

        # call creation hook
        self.at_creation()

    def add(self, data_handler, groups=None):
        """
        Add a new handler to data set.
        """
        key = (data_handler.app_name(), data_handler.model_name(),)
        self._handler_dict[key] = data_handler
        for group in groups:
            if group not in self._groups:
                # set data handlers by order
                self._groups[group] = []
            self._groups[group].append(data_handler)

    def data(self, model_name, app_name=None):
        """
        Get a data handler by model name.
        """
        if not app_name:
            app_name = settings.WORLD_DATA_APP
        key = (app_name, model_name,)
        return self._handler_dict.get(key, None)
        
    def group(self, group_name):
        """
        Get all models in this group.
        """
        if group_name not in self._groups:
            return None
            
        return self._groups[group_name]

    def at_creation(self):
        """
        Called on init.
        """
        pass

    def load_worlddata(self):
        """
        Load world data handlers.
        """
        # System settings
        self.add(SystemDataHandler("class_categories"), ("file_data", "system_data",))
        self.add(SystemDataHandler("typeclasses"), ("file_data", "system_data", "typeclasses"))
        self.add(SystemDataHandler("event_types"), ("file_data", "system_data",))
        self.add(SystemDataHandler("event_trigger_types"), ("file_data", "system_data",))
        self.add(SystemDataHandler("quest_objective_types"), ("file_data", "system_data",))
        self.add(SystemDataHandler("quest_dependency_types"), ("file_data", "system_data",))
        self.add(LocalizedStringsHandler("localized_strings"), ("file_data", "system_data",))

        # Basic settings
        self.add(FileDataHandler("equipment_types"), ("file_data", "basic_data",))
        self.add(FileDataHandler("equipment_positions"), ("file_data", "basic_data",))
        self.add(FileDataHandler("character_careers"), ("file_data", "basic_data",))
        self.add(FileDataHandler("career_equipments"), ("file_data", "basic_data",))
        self.add(FileDataHandler("character_models"), ("file_data", "basic_data",))
        self.add(FileDataHandler("custom_tables"), ("file_data", "basic_data",))
        self.add(FileDataHandler("custom_fields"), ("file_data", "basic_data",))

        # Objects data
        self.add(FileDataHandler("world_areas"), ("file_data", "object_data",))
        self.add(FileDataHandler("world_rooms"), ("file_data", "object_data",))
        self.add(FileDataHandler("world_exits"), ("file_data", "object_data",))
        self.add(FileDataHandler("world_objects"), ("file_data", "object_data",))
        self.add(FileDataHandler("world_npcs"), ("file_data", "object_data",))
        self.add(FileDataHandler("common_objects"), ("file_data", "object_data",))
        self.add(FileDataHandler("common_characters"), ("file_data", "object_data",))
        self.add(FileDataHandler("skills"), ("file_data", "object_data",))
        self.add(FileDataHandler("quests"), ("file_data", "object_data",))
        self.add(FileDataHandler("equipments"), ("file_data", "object_data",))
        self.add(FileDataHandler("foods"), ("file_data", "object_data",))
        self.add(FileDataHandler("skill_books"), ("file_data", "object_data",))
        # self.add(FileDataHandler("shops"), ("file_data", "object_data",))
        # self.add(FileDataHandler("shop_goods"), ("file_data", "object_data",))
        
        # Object additional data
        self.add(FileDataHandler("exit_locks"), ("file_data", "additional_data",))
        self.add(FileDataHandler("two_way_exits"), ("file_data", "additional_data",))
        self.add(FileDataHandler("object_creators"), ("file_data", "additional_data",))

        # Other data
        self.add(FileDataHandler("game_settings"), ("file_data", "other_data",))
        self.add(FileDataHandler("creator_loot_list"), ("file_data", "other_data",))
        self.add(FileDataHandler("character_loot_list"), ("file_data", "other_data",))
        self.add(FileDataHandler("quest_reward_list"), ("file_data", "other_data",))
        self.add(FileDataHandler("quest_objectives"), ("file_data", "other_data",))
        self.add(FileDataHandler("quest_dependencies"), ("file_data", "other_data",))
        self.add(FileDataHandler("event_data"), ("file_data", "other_data",))
        self.add(FileDataHandler("dialogues"), ("file_data", "other_data",))
        self.add(FileDataHandler("dialogue_sentences"), ("file_data", "other_data",))
        self.add(FileDataHandler("dialogue_relations"), ("file_data", "other_data",))
        self.add(FileDataHandler("npc_dialogues"), ("file_data", "other_data",))
        self.add(FileDataHandler("dialogue_quest_dependencies"), ("file_data", "other_data",))
        self.add(FileDataHandler("default_objects"), ("file_data", "other_data",))
        self.add(FileDataHandler("default_skills"), ("file_data", "other_data",))
        # self.add(FileDataHandler("npc_shops"), ("file_data", "other_data",))
        self.add(FileDataHandler("image_resources"), ("file_data", "other_data",))
        self.add(FileDataHandler("icon_resources"), ("file_data", "other_data",))

        # Event additional data
        self.add(FileDataHandler("event_attacks"), ("file_data", "event_additional_data",))
        self.add(FileDataHandler("event_dialogues"), ("file_data", "event_additional_data",))


# Data sets
DATA_SETS = class_from_module(settings.DATA_SETS)()
