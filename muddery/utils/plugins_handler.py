"""
This model translates default strings into localized strings.
"""

from __future__ import print_function

from django.conf import settings
from evennia.utils import logger
from muddery.worlddata.data_sets import DATA_SETS


class PluginsHandler(object):
    """
    This model translates default strings into localized strings.
    """
    def __init__(self):
        """
        Initialize handler
        """
        self.plugins = {}

    def clear(self):
        """
        Clear data.
        """
        self.plugins = {}

    def reload(self):
        """
        Reload all plugins.
        """
        logger.log_info("Reload plugins.")
        
        self.clear()
        
        for plugin_name in settings.PLUGINS:
            self.load_plugin(plugin_name)
            
    def load_plugin(self, plugin_name):
        """
        Load a plugin.
        
        Args:
            plugin: (string) plugin's name.
        """
        logger.log_info("Loading plugin: %s" % plugin_name)
        module_path = settings.MUDDERY_PLUGINS_DIR + "." + plugin_name + ".handler"
        module = __import__(module_path, fromlist=["handler"])
        handler = module.HANDLER
        if handler:
            self.plugins[plugin_name] = handler
            handler.at_init()
            logger.log_info("%s loaded." % plugin_name)
            
    def load_data(self):
        """
        Call all plugin's at_loading_data.
        """
        for name, plugin in self.plugins.iteritems():
            try:
                plugin.at_load_data()
                logger.log_info("%s's data loaded." % name)
            except Exception, e:
                err_message = "Can not load data of plugin '%s': %s" % (name, e)
                logger.log_tracemsg(err_message)


# main plugins handler
PLUGINS_HANDLER = PluginsHandler()
