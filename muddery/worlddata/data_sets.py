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
        # System settings
        self.class_categories = SystemDataHandler("class_categories")
        self.typeclasses = SystemDataHandler("typeclasses")
        self.event_types = SystemDataHandler("event_types")
        self.event_trigger_types = SystemDataHandler("event_trigger_types")
        self.quest_objective_types = SystemDataHandler("quest_objective_types")
        self.quest_dependency_types = SystemDataHandler("quest_dependency_types")
        self.localized_strings = LocalizedStringsHandler("localized_strings")

        self.system_data = [self.class_categories,
                            self.typeclasses,
                            self.event_types,
                            self.event_trigger_types,
                            self.quest_objective_types,
                            self.quest_dependency_types,
                            self.localized_strings]

        # Basic settings
        self.equipment_types = FileDataHandler("equipment_types")
        self.equipment_positions = FileDataHandler("equipment_positions")
        self.character_careers = FileDataHandler("character_careers")
        self.career_equipments = FileDataHandler("career_equipments")
        self.character_models = FileDataHandler("character_models")
        self.custom_tables = FileDataHandler("custom_tables")
        self.custom_fields = FileDataHandler("custom_fields")
        
        self.basic_data = [self.equipment_types,
                           self.equipment_positions,
                           self.character_careers,
                           self.career_equipments,
                           self.character_models,
                           self.custom_tables,
                           self.custom_fields]

        # Objects data
        self.world_areas = FileDataHandler("world_areas")
        self.world_rooms = FileDataHandler("world_rooms")
        self.world_exits = FileDataHandler("world_exits")
        self.world_objects = FileDataHandler("world_objects")
        self.world_npcs = FileDataHandler("world_npcs")
        self.common_objects = FileDataHandler("common_objects")
        self.common_characters = FileDataHandler("common_characters")
        self.skills = FileDataHandler("skills")
        self.quests = FileDataHandler("quests")
        self.equipments = FileDataHandler("equipments")
        self.foods = FileDataHandler("foods")
        self.skill_books = FileDataHandler("skill_books")
        self.shops = FileDataHandler("shops")
        self.shop_goods = FileDataHandler("shop_goods")

        self.object_data = [self.world_areas,
                            self.world_rooms,
                            self.world_exits,
                            self.world_objects,
                            self.world_npcs,
                            self.common_objects,
                            self.common_characters,
                            self.skills,
                            self.quests,
                            self.equipments,
                            self.foods,
                            self.skill_books,
                            self.shops,
                            self.shop_goods]

        # Object additional data
        # self.exit_locks = FileDataHandler("exit_locks")
        self.two_way_exits = FileDataHandler("two_way_exits")
        self.object_creators = FileDataHandler("object_creators")
        
        self.object_additional_data = [self.two_way_exits,
                                       self.object_creators]

        # Other data
        self.game_settings = FileDataHandler("game_settings")
        self.creator_loot_list = FileDataHandler("creator_loot_list")
        self.character_loot_list = FileDataHandler("character_loot_list")
        self.quest_reward_list = FileDataHandler("quest_reward_list")
        self.quest_objectives = FileDataHandler("quest_objectives")
        self.quest_dependencies = FileDataHandler("quest_dependencies")
        self.event_data = FileDataHandler("event_data")
        self.dialogues = FileDataHandler("dialogues")
        self.dialogue_sentences = FileDataHandler("dialogue_sentences")
        self.dialogue_relations = FileDataHandler("dialogue_relations")
        self.npc_dialogues = FileDataHandler("npc_dialogues")
        self.dialogue_quest_dependencies = FileDataHandler("dialogue_quest_dependencies")
        self.default_objects = FileDataHandler("default_objects")
        self.default_skills = FileDataHandler("default_skills")
        self.npc_shops = FileDataHandler("npc_shops")
        self.image_resources = FileDataHandler("image_resources")
        self.icon_resources = FileDataHandler("icon_resources")

        self.other_data = [self.game_settings,
                           self.creator_loot_list,
                           self.character_loot_list,
                           self.quest_reward_list,
                           self.quest_objectives,
                           self.quest_dependencies,
                           self.event_data,
                           self.dialogues,
                           self.dialogue_sentences,
                           self.dialogue_relations,
                           self.npc_dialogues,
                           self.dialogue_quest_dependencies,
                           self.default_objects,
                           self.default_skills,
                           self.shop_goods,
                           self.npc_shops,
                           self.image_resources,
                           self.icon_resources]

        # Event additional data
        self.event_attacks = FileDataHandler("event_attacks")
        self.event_dialogues = FileDataHandler("event_dialogues")

        self.event_additional_data = [self.event_attacks,
                                      self.event_dialogues]
                                      
        # Custom data
        self.custom_records = DataHandler("custom_records")

        # all file data handlers
        self.file_data_handlers = []
        
        # data handler dict
        self.handler_dict = {}

        # update data dict after hook
        self.update_data_sets()
        
        # call creation hook
        self.at_creation()

    def update_data_sets(self):
        # all data handlers
        self.file_data_handlers = []
        self.file_data_handlers.extend(self.system_data)
        self.file_data_handlers.extend(self.basic_data)
        self.file_data_handlers.extend(self.object_data)
        self.file_data_handlers.extend(self.object_additional_data)
        self.file_data_handlers.extend(self.other_data)
        self.file_data_handlers.extend(self.event_additional_data)
        
        # data handler dict
        self.handler_dict = {}
        for data_handler in self.file_data_handlers:
            self.handler_dict[data_handler.model_name()] = data_handler
            
        # add custom data handler

    def add_data_handler(self, group, data_handler):
        if group:
            group.append(data_handler)

        self.handler_dict[data_handler.model_name()] = data_handler

    def get_handler(self, model_name):
        """
        Get a data handler by model name.
        """
        return self.handler_dict.get(model_name, None)

    def at_creation(self):
        pass


# Data sets
DATA_SETS = class_from_module(settings.DATA_SETS)()
