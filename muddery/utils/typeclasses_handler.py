"""
This model translates default strings into localized strings.
"""

from __future__ import print_function

from evennia.utils import logger


class TypeclassesHandler(object):
    """
    This model stores all typeclasses pathes.
    """
    def __init__(self):
        """
        Initialize handler
        """
        self.dict = {}
        self.category = {}

    def add_group(self, data_handlers):
        """
        Add a group of typeclass's data handlers.
        """
        for data_handler in data_handlers:
            try:
                # load data
                for record in data_handler.all():
                    data = {"key": record.key,
                            "path": record.path,
                            "name": record.name,
                            "desc": record.desc,
                            "category": record.category}
                    self.dict[record.key] = data        
            except Exception, e:
                print("Can not add typeclass: %s" % e)
            
        # Typeclass's category may changed, so reset categories.
        self.category = {}
        for data in self.dict.values():
            if data["category"] not in self.category:
                self.category[data["category"]] = []
            self.category[data["category"]].append(data)
            
        print("classes: %s" % self.dict)

    def get_data(self, key):
        """
        Get typeclass's data.
        """
        if key not in self.dict:
            return None
        return self.dict[key]

    def get_path(self, key):
        """
        Get typeclass's path.
        """
        if key not in self.dict:
            return None
        return self.dict[key]["path"]

    def get_category(self, category):
        """
        Get typeclasses of this category.
        """
        if category not in self.category:
            return None
        return self.category[category]


# typeclasses handler
TYPECLASSES_HANDLER = TypeclassesHandler()
