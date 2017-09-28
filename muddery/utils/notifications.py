"""
Define notification utils.
"""

from muddery.utils.plugins_handler import PLUGINS_HANDLER


def notification(func):
    # Plugin's notification decorator. Call plugin's notification handler after the function.
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        result = PLUGINS_HANDLER.at_notification(self.db.typeclass_key,
                                                 func.__name__,
                                                 self,
                                                 args,
                                                 kwargs,
                                                 result)
        return result

    return wrapper