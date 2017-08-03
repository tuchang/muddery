
from django.contrib.admin.forms import forms
from muddery.utils.typeclasses_handler import TYPECLASSES_HANDLER
from muddery.utils.localiztion_handler import localize_form_fields
from muddery.worlddata.data_sets import DATA_SETS


def get_all_pocketable_objects():
    """
    Get all objects that can be put in player's pockets.
    """
    # available objects are common objects, foods skill books or equipments
    objects = DATA_SETS.data("common_objects").all()
    choices = [(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects]

    foods = DATA_SETS.data("foods").all()
    choices.extend([(obj.key, obj.name + " (" + obj.key + ")") for obj in foods])

    skill_books = DATA_SETS.data("skill_books").all()
    choices.extend([(obj.key, obj.name + " (" + obj.key + ")") for obj in skill_books])

    equipments = DATA_SETS.data("equipments").all()
    choices.extend([(obj.key, obj.name + " (" + obj.key + ")") for obj in equipments])

    return choices

        
class GameSettingsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(GameSettingsForm, self).__init__(*args, **kwargs)
        
        choices = [("", "---------")]
        objects = DATA_SETS.data("world_rooms").all()
        choices.extend([(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects])
        self.fields['default_home_key'] = forms.ChoiceField(choices=choices, required=False)
        self.fields['start_location_key'] = forms.ChoiceField(choices=choices, required=False)
        self.fields['default_player_home_key'] = forms.ChoiceField(choices=choices, required=False)

        choices = [("", "---------")]
        objects = DATA_SETS.data("common_characters").filter(typeclass="CLASS_PLAYER")
        choices.extend([(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects])
        self.fields['default_player_character_key'] = forms.ChoiceField(choices=choices, required=False)

        localize_form_fields(self)

    class Meta:
        model = DATA_SETS.data("game_settings")._model
        fields = '__all__'
        list_template = "common_list.html"
        form_template = "common_form.html"


class ClassCategoriesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ClassCategoriesForm, self).__init__(*args, **kwargs)
        localize_form_fields(self)

    class Meta:
        model = DATA_SETS.data("class_categories")._model
        fields = '__all__'
        desc = 'Categories of classes.'
        list_template = "common_list.html"
        form_template = "common_form.html"


class TypeclassesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TypeclassesForm, self).__init__(*args, **kwargs)

        objects = DATA_SETS.data("class_categories").objects.all()
        choices = [(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects]
        self.fields['category'] = forms.ChoiceField(choices=choices)

        localize_form_fields(self)
        
    class Meta:
        model = DATA_SETS.data("typeclasses")._model
        fields = '__all__'


class EquipmentTypesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EquipmentTypesForm, self).__init__(*args, **kwargs)
        localize_form_fields(self)

    class Meta:
        model = DATA_SETS.data("equipment_types")._model
        fields = '__all__'


class EquipmentPositionsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EquipmentPositionsForm, self).__init__(*args, **kwargs)
        localize_form_fields(self)

    class Meta:
        model = DATA_SETS.data("equipment_positions")._model
        fields = '__all__'


class CharacterCareersForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CharacterCareersForm, self).__init__(*args, **kwargs)
        localize_form_fields(self)

    class Meta:
        model = DATA_SETS.data("character_careers")._model
        fields = '__all__'


class QuestObjectiveTypesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(QuestObjectiveTypesForm, self).__init__(*args, **kwargs)
        localize_form_fields(self)

    class Meta:
        model = DATA_SETS.data("quest_objective_types")._model
        fields = '__all__'


class EventTypesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EventTypesForm, self).__init__(*args, **kwargs)
        localize_form_fields(self)

    class Meta:
        model = DATA_SETS.data("event_types")._model
        fields = '__all__'


class EventTriggerTypes(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EventTriggerTypes, self).__init__(*args, **kwargs)
        localize_form_fields(self)

    class Meta:
        model = DATA_SETS.data("event_trigger_types")._model
        fields = '__all__'


class QuestDependencyTypesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(QuestDependencyTypesForm, self).__init__(*args, **kwargs)
        localize_form_fields(self)

    class Meta:
        model = DATA_SETS.data("quest_dependency_types")._model
        fields = '__all__'


class WorldAreasForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(WorldAreasForm, self).__init__(*args, **kwargs)

        objects = TYPECLASSES_HANDLER.get_category("CATE_AREA")
        choices = [(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects]
        self.fields['typeclass'] = forms.ChoiceField(choices=choices)

        choices = [("", "---------")]
        objects = DATA_SETS.data("image_resources").objects.all()
        choices.extend([(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects])
        self.fields['background'] = forms.ChoiceField(choices=choices, required=False)

        localize_form_fields(self)

    class Meta:
        model = DATA_SETS.data("world_areas")._model
        fields = '__all__'
        
    
class WorldRoomsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(WorldRoomsForm, self).__init__(*args, **kwargs)

        objects = TYPECLASSES_HANDLER.get_category("CATE_ROOM")
        choices = [(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects]
        self.fields['typeclass'] = forms.ChoiceField(choices=choices)

        choices = [("", "---------")]
        objects = DATA_SETS.data("world_areas").objects.all()
        choices.extend([(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects])
        self.fields['location'] = forms.ChoiceField(choices=choices)

        choices = [("", "---------")]
        objects = DATA_SETS.data("icon_resources").objects.all()
        choices.extend([(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects])
        self.fields['icon'] = forms.ChoiceField(choices=choices, required=False)

        choices = [("", "---------")]
        objects = DATA_SETS.data("image_resources").objects.all()
        choices.extend([(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects])
        self.fields['background'] = forms.ChoiceField(choices=choices, required=False)

        localize_form_fields(self)

    class Meta:
        model = DATA_SETS.data("world_rooms")._model
        fields = '__all__'


class WorldExitsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(WorldExitsForm, self).__init__(*args, **kwargs)

        objects = TYPECLASSES_HANDLER.get_category("CATE_EXIT")
        choices = [(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects]
        self.fields['typeclass'] = forms.ChoiceField(choices=choices)

        objects = DATA_SETS.data("world_rooms").objects.all()
        choices = [(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects]
        self.fields['location'] = forms.ChoiceField(choices=choices)
        self.fields['destination'] = forms.ChoiceField(choices=choices)

        localize_form_fields(self)

    class Meta:
        model = DATA_SETS.data("world_exits")._model
        fields = '__all__'


class ExitLocksForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ExitLocksForm, self).__init__(*args, **kwargs)

        #objects = models.world_exits.objects.filter(typeclass="CLASS_LOCKED_EXIT")
        #choices = [(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects]
        #self.fields['key'] = forms.ChoiceField(choices=choices)

        localize_form_fields(self)

    class Meta:
        model = DATA_SETS.data("exit_locks")._model
        fields = '__all__'



class TwoWayExitsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TwoWayExitsForm, self).__init__(*args, **kwargs)

        #objects = models.world_exits.objects.filter(typeclass="CLASS_LOCKED_EXIT")
        #choices = [(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects]
        #self.fields['key'] = forms.ChoiceField(choices=choices)

        localize_form_fields(self)

    class Meta:
        model = DATA_SETS.data("two_way_exits")._model
        fields = '__all__'


class WorldObjectsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(WorldObjectsForm, self).__init__(*args, **kwargs)

        objects = TYPECLASSES_HANDLER.get_data("CLASS_WORLD_OBJECT")
        choices = [(objects["key"], objects["name"] + " (" + objects["key"] + ")")]
        objects = TYPECLASSES_HANDLER.get_data("CLASS_OBJECT_CREATOR")
        choices.append((objects["key"], objects["name"] + " (" + objects["key"] + ")"))
        self.fields['typeclass'] = forms.ChoiceField(choices=choices)

        objects = DATA_SETS.data("world_rooms").objects.all()
        choices = [(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects]
        self.fields['location'] = forms.ChoiceField(choices=choices)
        
        choices = [("", "---------")]
        objects = DATA_SETS.data("icon_resources").objects.all()
        choices.extend([(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects])
        self.fields['icon'] = forms.ChoiceField(choices=choices, required=False)

        localize_form_fields(self)

    class Meta:
        model = DATA_SETS.data("world_objects")._model
        fields = '__all__'


class WorldNPCsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(WorldNPCsForm, self).__init__(*args, **kwargs)

        # NPC's typeclass
        objects = TYPECLASSES_HANDLER.get_category("CATE_CHARACTER")
        choices = [(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects]
        self.fields['typeclass'] = forms.ChoiceField(choices=choices)
        
        # NPC's location
        objects = DATA_SETS.data("world_rooms").objects.all()
        choices = [(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects]
        self.fields['location'] = forms.ChoiceField(choices=choices)
        
        # NPC's model
        choices = [("", "---------")]
        objects = DATA_SETS.data("character_models").objects.all()
        model_keys = set([obj.key for obj in objects])
        choices.extend([(model_key, model_key) for model_key in model_keys])
        self.fields['model'] = forms.ChoiceField(choices=choices, required=False)
        
        # NPC's icon
        choices = [("", "---------")]
        objects = DATA_SETS.data("icon_resources").objects.all()
        choices.extend([(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects])
        self.fields['icon'] = forms.ChoiceField(choices=choices, required=False)

        localize_form_fields(self)

    class Meta:
        model = DATA_SETS.data("world_npcs")._model
        fields = '__all__'


class ObjectCreatorsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ObjectCreatorsForm, self).__init__(*args, **kwargs)

        #objects = models.world_objects.objects.filter(typeclass="CLASS_OBJECT_CREATOR")
        #choices = [(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects]
        #self.fields['key'] = forms.ChoiceField(choices=choices)

        localize_form_fields(self)

    class Meta:
        model = DATA_SETS.data("object_creators")._model
        fields = '__all__'


class CreatorLootListForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreatorLootListForm, self).__init__(*args, **kwargs)

        # providers must be object_creators
        objects = DATA_SETS.data("world_objects").objects.filter(typeclass="CLASS_OBJECT_CREATOR")
        choices = [(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects]
        self.fields['provider'] = forms.ChoiceField(choices=choices)

        # available objects
        choices = get_all_pocketable_objects()
        self.fields['object'] = forms.ChoiceField(choices=choices)
        
        # depends on quest
        choices = [("", "---------")]
        objects = DATA_SETS.data("quests").objects.all()
        choices.extend([(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects])
        self.fields['quest'] = forms.ChoiceField(choices=choices, required=False)

        localize_form_fields(self)

    class Meta:
        model = DATA_SETS.data("creator_loot_list")._model
        fields = '__all__'


class CharacterLootListForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CharacterLootListForm, self).__init__(*args, **kwargs)

        # providers can be world_npc or common_character
        npcs = DATA_SETS.data("world_npcs").objects.all()
        choices = [(obj.key, obj.name + " (" + obj.key + ")") for obj in npcs]

        characters = DATA_SETS.data("common_characters").objects.all()
        choices.extend([(obj.key, obj.name + " (" + obj.key + ")") for obj in characters])

        self.fields['provider'] = forms.ChoiceField(choices=choices)

        # available objects
        choices = get_all_pocketable_objects()
        self.fields['object'] = forms.ChoiceField(choices=choices)

        # depends on quest
        choices = [("", "---------")]
        objects = DATA_SETS.data("quests").objects.all()
        choices.extend([(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects])
        self.fields['quest'] = forms.ChoiceField(choices=choices, required=False)

        localize_form_fields(self)
        
    class Meta:
        model = DATA_SETS.data("character_loot_list")._model
        fields = '__all__'


class QuestRewardListForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(QuestRewardListForm, self).__init__(*args, **kwargs)

        # providers must be object_creators
        objects = DATA_SETS.data("quests").objects.all()
        choices = [(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects]
        self.fields['provider'] = forms.ChoiceField(choices=choices)

        # available objects
        choices = get_all_pocketable_objects()
        self.fields['object'] = forms.ChoiceField(choices=choices)
        
        # depends on quest
        choices = [("", "---------")]
        objects = DATA_SETS.data("quests").objects.all()
        choices.extend([(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects])
        self.fields['quest'] = forms.ChoiceField(choices=choices, required=False)

        localize_form_fields(self)

    class Meta:
        model = DATA_SETS.data("quest_reward_list")._model
        fields = '__all__'


class CommonObjectsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommonObjectsForm, self).__init__(*args, **kwargs)

        objects = TYPECLASSES_HANDLER.get_category("CATE_OBJECT")
        choices = [(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects]
        self.fields['typeclass'] = forms.ChoiceField(choices=choices)
        
        choices = [("", "---------")]
        objects = DATA_SETS.data("icon_resources").objects.all()
        choices.extend([(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects])
        self.fields['icon'] = forms.ChoiceField(choices=choices, required=False)

        localize_form_fields(self)

    class Meta:
        model = DATA_SETS.data("common_objects")._model
        fields = '__all__'


class FoodsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FoodsForm, self).__init__(*args, **kwargs)
        
        objects = TYPECLASSES_HANDLER.get_data("CLASS_FOOD")
        choices = [(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects]
        self.fields['typeclass'] = forms.ChoiceField(choices=choices)
        
        choices = [("", "---------")]
        objects = DATA_SETS.data("icon_resources").objects.all()
        choices.extend([(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects])
        self.fields['icon'] = forms.ChoiceField(choices=choices, required=False)

        localize_form_fields(self)
        # FOOD_ATTRIBUTES_INFO.set_form_fields(self)

    class Meta:
        model = DATA_SETS.data("foods")._model
        fields = '__all__'
        

class SkillBooksForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SkillBooksForm, self).__init__(*args, **kwargs)
        
        objects = TYPECLASSES_HANDLER.get_data("CLASS_SKILL_BOOK")
        choices = [(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects]
        self.fields['typeclass'] = forms.ChoiceField(choices=choices)
        
        # skills
        objects = DATA_SETS.data("skills").objects.all()
        choices = [(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects]
        self.fields['skill'] = forms.ChoiceField(choices=choices)
        
        # icons
        choices = [("", "---------")]
        objects = DATA_SETS.data("icon_resources").objects.all()
        choices.extend([(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects])
        self.fields['icon'] = forms.ChoiceField(choices=choices, required=False)

        localize_form_fields(self)

    class Meta:
        model = DATA_SETS.data("skill_books")._model
        fields = '__all__'


class CharacterModelsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CharacterModelsForm, self).__init__(*args, **kwargs)
        localize_form_fields(self)
        # CHARACTER_ATTRIBUTES_INFO.set_form_fields(self)

    class Meta:
        model = DATA_SETS.data("character_models")._model
        fields = '__all__'


class CommonCharacterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommonCharacterForm, self).__init__(*args, **kwargs)

        objects = TYPECLASSES_HANDLER.get_category("CATE_CHARACTER")
        choices = [(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects]
        self.fields['typeclass'] = forms.ChoiceField(choices=choices)

        # models
        choices = [("", "---------")]
        objects = DATA_SETS.data("character_models").objects.all()
        model_keys = set([obj.key for obj in objects])
        choices.extend([(model_key, model_key) for model_key in model_keys])
        self.fields['model'] = forms.ChoiceField(choices=choices, required=False)
        
        choices = [("", "---------")]
        objects = DATA_SETS.data("icon_resources").objects.all()
        choices.extend([(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects])
        self.fields['icon'] = forms.ChoiceField(choices=choices, required=False)

        localize_form_fields(self)

    class Meta:
        model = DATA_SETS.data("common_characters")._model
        fields = '__all__'


class DefaultObjectsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DefaultObjectsForm, self).__init__(*args, **kwargs)

        # all character's models
        character_models = set([record.key for record in DATA_SETS.data("character_models").objects.all()])
        choices = [(key, key) for key in character_models]
        self.fields['character'] = forms.ChoiceField(choices=choices)

        # available objects
        choices = get_all_pocketable_objects()
        self.fields['object'] = forms.ChoiceField(choices=choices)

        localize_form_fields(self)
        
    class Meta:
        model = DATA_SETS.data("default_objects")._model
        fields = '__all__'


class SkillsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SkillsForm, self).__init__(*args, **kwargs)

        objects = TYPECLASSES_HANDLER.get_category("CATE_SKILL")
        choices = [(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects]
        self.fields['typeclass'] = forms.ChoiceField(choices=choices)
        
        choices = [("", "---------")]
        objects = DATA_SETS.data("icon_resources").objects.all()
        choices.extend([(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects])
        self.fields['icon'] = forms.ChoiceField(choices=choices, required=False)

        localize_form_fields(self)

    class Meta:
        model = DATA_SETS.data("skills")._model
        fields = '__all__'


class DefaultSkillsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DefaultSkillsForm, self).__init__(*args, **kwargs)

        # all character's models
        character_models = set([record.key for record in DATA_SETS.data("character_models").objects.all()])
        choices = [(key, key) for key in character_models]
        self.fields['character'] = forms.ChoiceField(choices=choices)

        objects = DATA_SETS.data("skills").objects.all()
        choices = [(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects]
        self.fields['skill'] = forms.ChoiceField(choices=choices)

        localize_form_fields(self)
        
    class Meta:
        model = DATA_SETS.data("default_skills")._model
        fields = '__all__'


class NPCDialoguesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NPCDialoguesForm, self).__init__(*args, **kwargs)

        # All NPCs.
        objects = DATA_SETS.data("world_npcs").objects.all()
        choices = [(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects]
        self.fields['npc'] = forms.ChoiceField(choices=choices)
        
        objects = DATA_SETS.data("dialogues").objects.all()
        choices = [(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects]
        self.fields['dialogue'] = forms.ChoiceField(choices=choices)

        localize_form_fields(self)

    class Meta:
        model = DATA_SETS.data("npc_dialogues")._model
        fields = '__all__'


class QuestsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(QuestsForm, self).__init__(*args, **kwargs)

        objects = TYPECLASSES_HANDLER.get_category("CATE_QUEST")
        choices = [(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects]
        self.fields['typeclass'] = forms.ChoiceField(choices=choices)

        localize_form_fields(self)

    class Meta:
        model = DATA_SETS.data("quests")._model
        fields = '__all__'


class QuestObjectivesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(QuestObjectivesForm, self).__init__(*args, **kwargs)

        objects = DATA_SETS.data("quests").objects.all()
        choices = [(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects]
        self.fields['quest'] = forms.ChoiceField(choices=choices)

        objects = DATA_SETS.data("quest_objective_types").objects.all()
        choices = [(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects]
        self.fields['type'] = forms.ChoiceField(choices=choices)

        localize_form_fields(self)

    class Meta:
        model = DATA_SETS.data("quest_objectives")._model
        fields = '__all__'


class QuestDependenciesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(QuestDependenciesForm, self).__init__(*args, **kwargs)

        objects = DATA_SETS.data("quests").objects.all()
        choices = [(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects]
        self.fields['quest'] = forms.ChoiceField(choices=choices)
        self.fields['dependency'] = forms.ChoiceField(choices=choices)
        
        objects = DATA_SETS.data("quest_dependency_types").objects.all()
        choices = [(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects]
        self.fields['type'] = forms.ChoiceField(choices=choices)

        localize_form_fields(self)

    class Meta:
        model = DATA_SETS.data("quest_dependencies")._model
        fields = '__all__'


class DialogueQuestDependenciesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DialogueQuestDependenciesForm, self).__init__(*args, **kwargs)

        objects = DATA_SETS.data("dialogues").objects.all()
        choices = [(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects]
        self.fields['dialogue'] = forms.ChoiceField(choices=choices)
        
        objects = DATA_SETS.data("quests").objects.all()
        choices = [(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects]
        self.fields['dependency'] = forms.ChoiceField(choices=choices)
        
        objects = DATA_SETS.data("quest_dependency_types").objects.all()
        choices = [(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects]
        self.fields['type'] = forms.ChoiceField(choices=choices)

        localize_form_fields(self)

    class Meta:
        model = DATA_SETS.data("dialogue_quest_dependencies")._model
        fields = '__all__'


class EquipmentsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EquipmentsForm, self).__init__(*args, **kwargs)
        
        objects = TYPECLASSES_HANDLER.get_data("CLASS_EQUIPMENT")
        choices = [(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects]
        self.fields['typeclass'] = forms.ChoiceField(choices=choices)

        objects = DATA_SETS.data("equipment_positions").objects.all()
        choices = [(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects]
        self.fields['position'] = forms.ChoiceField(choices=choices)
        
        objects = DATA_SETS.data("equipment_types").objects.all()
        choices = [(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects]
        self.fields['type'] = forms.ChoiceField(choices=choices)

        choices = [("", "---------")]
        objects = DATA_SETS.data("icon_resources").objects.all()
        choices.extend([(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects])
        self.fields['icon'] = forms.ChoiceField(choices=choices, required=False)
        
        localize_form_fields(self)
        # EQUIPMENT_ATTRIBUTES_INFO.set_form_fields(self)

    class Meta:
        model = DATA_SETS.data("equipments")._model
        fields = '__all__'


class CareerEquipmentsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CareerEquipmentsForm, self).__init__(*args, **kwargs)

        objects = DATA_SETS.data("character_careers").objects.all()
        choices = [(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects]
        self.fields['career'] = forms.ChoiceField(choices=choices)
        
        objects = DATA_SETS.data("equipment_types").objects.all()
        choices = [(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects]
        self.fields['equipment'] = forms.ChoiceField(choices=choices)

        localize_form_fields(self)

    class Meta:
        model = DATA_SETS.data("career_equipments")._model
        fields = '__all__'


class EventDataForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EventDataForm, self).__init__(*args, **kwargs)

        objects = DATA_SETS.data("event_types").objects.all()
        choices = [(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects]
        self.fields['type'] = forms.ChoiceField(choices=choices)

        objects = DATA_SETS.data("event_trigger_types").objects.all()
        choices = [(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects]
        self.fields['trigger_type'] = forms.ChoiceField(choices=choices)

        localize_form_fields(self)
        
    class Meta:
        model = DATA_SETS.data("event_data")._model
        fields = '__all__'


class EventAttacksForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EventAttacksForm, self).__init__(*args, **kwargs)

        objects = DATA_SETS.data("event_data").objects.filter(type="EVENT_ATTACK")
        choices = [(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects]
        self.fields['key'] = forms.ChoiceField(choices=choices)
        
        objects = DATA_SETS.data("common_characters").objects.all()
        choices = [(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects]
        self.fields['mob'] = forms.ChoiceField(choices=choices)

        localize_form_fields(self)

    class Meta:
        model = DATA_SETS.data("event_attacks")._model
        fields = '__all__'


class EventDialoguesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EventDialoguesForm, self).__init__(*args, **kwargs)

        objects = DATA_SETS.data("event_data").objects.filter(type="EVENT_DIALOGUE")
        choices = [(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects]
        self.fields['key'] = forms.ChoiceField(choices=choices)

        objects = DATA_SETS.data("dialogues").objects.all()
        choices = [(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects]
        self.fields['dialogue'] = forms.ChoiceField(choices=choices)

        # NPCs
        choices = [("", "---------")]
        objects = DATA_SETS.data("world_npcs").objects.all()
        choices.extend([(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects])
        self.fields['npc'] = forms.ChoiceField(choices=choices, required=False)

        localize_form_fields(self)
        
    class Meta:
        model = DATA_SETS.data("event_dialogues")._model
        fields = '__all__'


class DialoguesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DialoguesForm, self).__init__(*args, **kwargs)
        localize_form_fields(self)

    class Meta:
        model = DATA_SETS.data("dialogues")._model
        fields = '__all__'


class DialogueRelationsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DialogueRelationsForm, self).__init__(*args, **kwargs)

        objects = DATA_SETS.data("dialogues").objects.all()
        choices = [(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects]
        self.fields['dialogue'] = forms.ChoiceField(choices=choices)
        self.fields['next_dlg'] = forms.ChoiceField(choices=choices)

        localize_form_fields(self)

    class Meta:
        model = DATA_SETS.data("dialogue_relations")._model
        fields = '__all__'


class DialogueSentencesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DialogueSentencesForm, self).__init__(*args, **kwargs)

        objects = DATA_SETS.data("dialogues").objects.all()
        choices = [(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects]
        self.fields['dialogue'] = forms.ChoiceField(choices=choices)

        # dialogue's icon
        choices = [("", "---------")]
        objects = DATA_SETS.data("icon_resources").objects.all()
        choices.extend([(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects])
        self.fields['icon'] = forms.ChoiceField(choices=choices, required=False)
        
        choices = [("", "---------")]
        objects = DATA_SETS.data("quests").objects.all()
        choices.extend([(obj["key"], obj["name"] + " (" + obj["key"] + ")") for obj in objects])
        self.fields['provide_quest'] = forms.ChoiceField(choices=choices, required=False)
        self.fields['complete_quest'] = forms.ChoiceField(choices=choices, required=False)

        localize_form_fields(self)

    class Meta:
        model = DATA_SETS.data("dialogue_sentences")._model
        fields = '__all__'


class LocalizedStringsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LocalizedStringsForm, self).__init__(*args, **kwargs)
        localize_form_fields(self)

    class Meta:
        model = DATA_SETS.data("localized_strings")._model
        fields = '__all__'


class ImageResourcesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ImageResourcesForm, self).__init__(*args, **kwargs)
        localize_form_fields(self)

    class Meta:
        model = DATA_SETS.data("image_resources")._model
        fields = ('key', 'name', 'resource',)


class IconResourcesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(IconResourcesForm, self).__init__(*args, **kwargs)
        localize_form_fields(self)

    class Meta:
        model = DATA_SETS.data("icon_resources")._model
        fields = ('key', 'name', 'resource',)
