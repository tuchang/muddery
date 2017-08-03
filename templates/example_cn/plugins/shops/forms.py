
from django.contrib.admin.forms import forms
from muddery.utils.localiztion_handler import localize_form_fields
from muddery.worlddata.data_sets import DATA_SETS


class ShopsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ShopsForm, self).__init__(*args, **kwargs)
        
        objects = DATA_SETS.data("typeclasses").objects.filter(category="CATE_SHOP")
        choices = [(obj.key, obj.name + " (" + obj.key + ")") for obj in objects]
        self.fields['typeclass'] = forms.ChoiceField(choices=choices)
        
        choices = [("", "---------")]
        objects = DATA_SETS.data("icon_resources").objects.all()
        choices.extend([(obj.key, obj.name + " (" + obj.key + ")") for obj in objects])
        self.fields['icon'] = forms.ChoiceField(choices=choices, required=False)
        
        localize_form_fields(self)
        
    class Meta:
        model = DATA_SETS.data("shops")._model
        fields = '__all__'


class ShopGoodsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ShopGoodsForm, self).__init__(*args, **kwargs)

        # all shops
        objects = DATA_SETS.data("shops").objects.all()
        choices = [(obj.key, obj.name + " (" + obj.key + ")") for obj in objects]
        self.fields['shop'] = forms.ChoiceField(choices=choices)

        # available objects
        choices = get_all_pocketable_objects()
        self.fields['object'] = forms.ChoiceField(choices=choices)

        # Goods typeclasses
        objects = DATA_SETS.data("typeclasses").objects.filter(category="CATE_SHOP_GOODS")
        choices = [(obj.key, obj.name + " (" + obj.key + ")") for obj in objects]
        self.fields['typeclass'] = forms.ChoiceField(choices=choices)

        # available units are common objects
        objects = DATA_SETS.data("common_objects").objects.all()
        choices = [(obj.key, obj.name + " (" + obj.key + ")") for obj in objects]
        self.fields['unit'] = forms.ChoiceField(choices=choices)

        localize_form_fields(self)
        
    class Meta:
        model = DATA_SETS.data("shop_goods")._model
        fields = '__all__'


class NPCShopsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NPCShopsForm, self).__init__(*args, **kwargs)

        # All NPCs.
        objects = DATA_SETS.data("world_npcs").objects.all()
        choices = [(obj.key, obj.name + " (" + obj.key + ")") for obj in objects]
        self.fields['npc'] = forms.ChoiceField(choices=choices)
        
        # All shops.
        objects = DATA_SETS.data("shops").objects.all()
        choices = [(obj.key, obj.name + " (" + obj.key + ")") for obj in objects]
        self.fields['shop'] = forms.ChoiceField(choices=choices)

        localize_form_fields(self)
        
    class Meta:
        model = DATA_SETS.data("npc_shops")._model
        fields = '__all__'
