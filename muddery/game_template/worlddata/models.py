from django.db import models
from muddery.worlddata.db import models as model_base


# ------------------------------------------------------------
#
# game's basic settings
#
# ------------------------------------------------------------
class game_settings(model_base.game_settings):
    """
    Game's basic settings.
    """
    pass


# ------------------------------------------------------------
#
# all objects
#
# ------------------------------------------------------------
class objects(model_base.objects):
    "All objects in the game."
    pass


# ------------------------------------------------------------
#
# world areas
#
# ------------------------------------------------------------
class world_areas(model_base.world_areas):
    "Rooms belongs to areas."
    pass
    

#------------------------------------------------------------
#
# store all rooms
#
#------------------------------------------------------------
class world_rooms(model_base.world_rooms):
    "Store all unique rooms."
    pass


#------------------------------------------------------------
#
# store all exits
#
#------------------------------------------------------------
class world_exits(model_base.world_exits):
    "Store all unique exits."
    pass


#------------------------------------------------------------
#
# store exit locks
#
#------------------------------------------------------------
class exit_locks(model_base.exit_locks):
    "Store all exit locks."
    pass


#------------------------------------------------------------
#
# store all objects
#
#------------------------------------------------------------
class world_objects(model_base.world_objects):
    "Store all unique objects."
    pass


#------------------------------------------------------------
#
# store all object creators
#
#------------------------------------------------------------
class object_creators(model_base.object_creators):
    "Store all object creators."
    pass


#------------------------------------------------------------
#
# object creator's loot list
#
#------------------------------------------------------------
class creator_loot_list(model_base.creator_loot_list):
    "Object creator's loot list"
    pass


#------------------------------------------------------------
#
# store all common objects
#
#------------------------------------------------------------
class common_objects(model_base.common_objects):
    "Store all common objects."
    pass


# ------------------------------------------------------------
#
# store all foods
#
# ------------------------------------------------------------
class foods(model_base.foods):
    "Foods inherit from common objects."
    pass


# ------------------------------------------------------------
#
# store all skill books
#
# ------------------------------------------------------------
class skill_books(model_base.skill_books):
    "Skill books inherit from common objects."
    pass
    

#------------------------------------------------------------
#
# store all equip_types
#
#------------------------------------------------------------
class equipment_types(model_base.equipment_types):
    "Store all equip types."
    pass


#------------------------------------------------------------
#
# store all equip_positions
#
#------------------------------------------------------------
class equipment_positions(model_base.equipment_positions):
    "Store all equip types."
    pass


#------------------------------------------------------------
#
# store all equipments
#
#------------------------------------------------------------
class equipments(model_base.equipments):
    "Store all equipments."
    pass


# ------------------------------------------------------------
#
# character attributes
#
# ------------------------------------------------------------
class character_attributes_info(model_base.character_attributes_info):
    "character attributes"
    pass


# ------------------------------------------------------------
#
# Equipment attribute's information.
#
# ------------------------------------------------------------
class equipment_attributes_info(model_base.equipment_attributes_info):
    "Equipment's all available attributes"
    pass


# ------------------------------------------------------------
#
# Food attribute's information.
#
# ------------------------------------------------------------
class food_attributes_info(model_base.food_attributes_info):
    "Food attribute's information."
    pass


#------------------------------------------------------------
#
# character levels
#
#------------------------------------------------------------
class character_models(model_base.character_models):
    "Store all character level informations."
    pass


#------------------------------------------------------------
#
# store all npcs
#
#------------------------------------------------------------
class world_npcs(model_base.world_npcs):
    "Store all unique objects."
    pass


#------------------------------------------------------------
#
# store common characters
#
#------------------------------------------------------------
class common_characters(model_base.common_characters):
    "Store all common characters."
    pass


#------------------------------------------------------------
#
# character's loot list
#
#------------------------------------------------------------
class character_loot_list(model_base.character_loot_list):
    "Character's loot list"
    pass


#------------------------------------------------------------
#
# character's default objects
#
#------------------------------------------------------------
class default_objects(model_base.default_objects):
    "Store character's default objects information."
    pass
    

# ------------------------------------------------------------
#
# shops
#
# ------------------------------------------------------------
class shops(model_base.shops):
    "Store all shops."
    pass
        
        
# ------------------------------------------------------------
#
# shop goods
#
# ------------------------------------------------------------
class shop_goods(model_base.shop_goods):
    "All goods that sold in shops."
    pass


# ------------------------------------------------------------
#
# npc shops
#
# ------------------------------------------------------------
class npc_shops(model_base.npc_shops):
    "Store npc's shops."
    pass
    
    
#------------------------------------------------------------
#
# store all skills
#
#------------------------------------------------------------
class skills(model_base.skills):
    "Store all skills."
    pass


# ------------------------------------------------------------
#
# skill types
#
# ------------------------------------------------------------
class skill_types(model_base.skill_types):
    "Skill's types."
    pass


#------------------------------------------------------------
#
# character skills
#
#------------------------------------------------------------
class default_skills(model_base.default_skills):
    "Store all character skill informations."
    pass


#------------------------------------------------------------
#
# store all quests
#
#------------------------------------------------------------
class quests(model_base.quests):
    "Store all dramas."
    pass


#------------------------------------------------------------
#
# quest's reward list
#
#------------------------------------------------------------
class quest_reward_list(model_base.quest_reward_list):
    "Quest's reward list"
    pass


#------------------------------------------------------------
#
# store quest objectives
#
#------------------------------------------------------------
class quest_objectives(model_base.quest_objectives):
    "Store all quest objectives."
    pass


#------------------------------------------------------------
#
# store quest dependencies
#
#------------------------------------------------------------
class quest_dependencies(model_base.quest_dependencies):
    "Store quest dependency."
    pass


#------------------------------------------------------------
#
# store event data
#
#------------------------------------------------------------
class event_data(model_base.event_data):
    "Store event data."
    pass


#------------------------------------------------------------
#
# store all dialogues
#
#------------------------------------------------------------
class dialogues(model_base.dialogues):
    "Store all dialogues."
    pass


#------------------------------------------------------------
#
# store dialogue quest dependencies
#
#------------------------------------------------------------
class dialogue_quest_dependencies(model_base.dialogue_quest_dependencies):
    "Store dialogue quest dependencies."
    pass


#------------------------------------------------------------
#
# store dialogue relations
#
#------------------------------------------------------------
class dialogue_relations(model_base.dialogue_relations):
    "Store dialogue relations."
    pass


#------------------------------------------------------------
#
# store dialogue sentences
#
#------------------------------------------------------------
class dialogue_sentences(model_base.dialogue_sentences):
    "Store dialogue sentences."
    pass


#------------------------------------------------------------
#
# store npc's dialogue
#
#------------------------------------------------------------
class npc_dialogues(model_base.npc_dialogues):
    "Store all dialogues."
    pass


# ------------------------------------------------------------
#
# event attack's data
#
# ------------------------------------------------------------
class action_attack(model_base.action_attack):
    "event attack's data"
    pass


#------------------------------------------------------------
#
# event dialogues
#
#------------------------------------------------------------
class action_dialogue(model_base.action_dialogue):
    "Store all event dialogues."
    pass


#------------------------------------------------------------
#
# event closes
#
#------------------------------------------------------------
class action_learn_skill(model_base.action_learn_skill):
    pass

    
#------------------------------------------------------------
#
# action to accept a quest
#
#------------------------------------------------------------
class action_accept_quest(model_base.action_accept_quest):
    pass


#------------------------------------------------------------
#
# action to turn in a quest
#
#------------------------------------------------------------
class action_turn_in_quest(model_base.action_turn_in_quest):
    pass

    
# ------------------------------------------------------------
#
# action to close an event
#
# ------------------------------------------------------------
class action_close_event(model_base.action_close_event):
    pass
    

# ------------------------------------------------------------
#
# condition descriptions
#
# ------------------------------------------------------------
class condition_desc(model_base.condition_desc):
    "Object descriptions in different conditions."
    pass


#------------------------------------------------------------
#
# localized strings
#
#------------------------------------------------------------
class localized_strings(model_base.localized_strings):
    "Store all system localized strings."
    pass


#------------------------------------------------------------
#
# image resources
#
#------------------------------------------------------------
class image_resources(model_base.image_resources):
    "Store all image resource's information."
    pass
