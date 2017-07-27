"""
This module defines available model types.
"""
import os
import glob
import traceback
from django.apps import apps
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from evennia.utils import logger
from muddery.utils import readers
from muddery.utils.exception import MudderyError
from muddery.worlddata.data_handler.file_data_handler import FileDataHandler


class LocalizedStringsHandler(FileDataHandler):
    """

    """
    def import_data(self, reader, **kwargs):
        """
        Import data to the model.

        Args:
            model_obj:
            reader:

        Returns:
            None
        """
        system_data = kwargs.get('system_data', False)

        line = 1
        try:
            # read title
            titles = reader.next()

            field_types = self.get_field_types(self._model, titles)

            category_index = -1
            origin_index = -1
            if system_data:
                # get pk's position
                for index, title in enumerate(titles):
                    if title == "category":
                        category_index = index
                    elif title == "origin":
                        origin_index = index
                if category_index == -1 and origin_index == -1:
                    print("Can not found data's key.")
                    return
                    
            line += 1

            # import values
            for values in reader:
                # skip blank lines
                blank_line = True
                for value in values:
                    if value:
                        blank_line = False
                        break
                if blank_line:
                    line += 1
                    continue

                record = self.parse_record(titles, field_types, values)
                category = values[category_index]
                origin = values[origin_index]

                # Merge system and custom data.
                if system_data:
                    # System data can not overwrite custom data.
                    if self._objects.filter(category=category, origin=origin, system_data=False).count() > 0:
                        continue

                    # Add system data flag.
                    record["system_data"] = True
                else:
                    # Custom data can not overwrite system data.
                    self._objects.filter(category=category, origin=origin, system_data=True).delete()

                data = self._model(**record)
                data.full_clean()
                data.save()
                line += 1

        except StopIteration:
            # reach the end of file, pass this exception
            pass
        except ValidationError, e:
            raise MudderyError(self.parse_error(e, line))
        except Exception, e:
            raise MudderyError("%s (model: %s, line: %s)" % (e, self._model_name, line))

    def import_from_path(self, path_name, **kwargs):
        # import data from default position
        super(LocalizedStringsHandler, self).import_from_path(path_name, **kwargs)

        # import all files in LOCALIZED_STRINGS_FOLDER
        dir_name = os.path.join(path_name,
                                settings.LOCALIZED_STRINGS_FOLDER,
                                settings.LANGUAGE_CODE)

        if os.path.isdir(dir_name):
            # Does not clear previous data.
            kwargs["clear"] = False
            for file_name in os.listdir(dir_name):
                file_name = os.path.join(dir_name, file_name)
                if os.path.isdir(file_name):
                    # if it is a folder
                    continue

                self.import_file(file_name, **kwargs)

    def clear_model_data(self, **kwargs):
        """
        Remove all data from db.

        Args:
            model_name: (string) db model's name.

        Returns:
            None
        """
        system_data = kwargs.get('system_data', False)
        
        # clear old data
        self._objects.filter(system_data=system_data).delete()
