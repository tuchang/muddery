"""
This model localize other models.
"""


def auto_generate_key(model):
    if not model.key:
        index = 0
        if model.id is not None:
            # Get this record's id.
            index = model.id
        else:
            try:
                # Get last id.
                query = model.__class__.objects.last()
                index = int(query.id)
                index += 1
            except Exception, e:
                pass

        model.key = model.__class__.__name__ + "_" + str(index)


def validate_object_key(model):
    """
    Check if the key exists. Object's key should be unique in all objects.
    """
    # Get models.
    from muddery.worlddata.data_sets import DATA_SETS
    for data_settings in DATA_SETS.group("object_data"):
        if data_settings.model_name() == model.__class__.__name__:
            # Models will validate unique values of its own,
            # so we do not validate them here.
            continue

        try:
            data_settings.model.objects.get(key=model.key)
        except Exception, e:
            continue

        error = ValidationError("The key '%(value)s' already exists in model %(model)s.",
                                code="unique",
                                params={"value": model.key, "model": data_settings.model_name()})
        raise ValidationError({"key": error})
