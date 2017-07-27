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


class SystemDataHandler(FileDataHandler):
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

            key_index = -1
            # get pk's position
            for index, title in enumerate(titles):
                if title == "key":
                    key_index = index
                    break
            if key_index == -1:
                print("Can not found system data's key.")
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
                key = values[key_index]

                # Merge system and custom data.
                if system_data:
                    # System data can not overwrite custom data.
                    if self._objects.filter(key=key, system_data=False).count() > 0:
                        continue

                    # Add system data flag.
                    record["system_data"] = True
                else:
                    # Custom data can not overwrite system data.
                    self._objects.filter(key=key, system_data=True).delete()

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
