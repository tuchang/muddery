"""
Master configuration file for Muddery.

NOTE: NO MODIFICATIONS SHOULD BE MADE TO THIS FILE!

All settings changes should be done by copy-pasting the variable and
its value to <gamedir>/conf/settings.py.

Hint: Don't copy&paste over more from this file than you actually want
to change.  Anything you don't copy&paste will thus retain its default
value - which may change as Muddery is developed. This way you can
always be sure of what you have changed and what is default behaviour.

"""

import os
from evennia.settings_default import EVENNIA_DIR, GAME_DIR
from evennia.settings_default import WEBSITE_TEMPLATE
from evennia.settings_default import INSTALLED_APPS


######################################################################
# Evennia base server config
######################################################################

# This is the name of your server.
SERVERNAME = "Muddery"

######################################################################
# Muddery base server config
######################################################################

MUDDERY_DIR = os.path.dirname(os.path.abspath(__file__))

# Place to put log files
LOG_DIR = os.path.join(GAME_DIR, "server", "logs")
SERVER_LOG_FILE = os.path.join(LOG_DIR, 'server.log')
PORTAL_LOG_FILE = os.path.join(LOG_DIR, 'portal.log')
HTTP_LOG_FILE = os.path.join(LOG_DIR, 'http_requests.log')

# This setting is no use any more, so set it to blank.
WEBSOCKET_CLIENT_URL = ""


######################################################################
# Evennia Database config
######################################################################

# Database config syntax:
# ENGINE - path to the the database backend. Possible choices are:
#            'django.db.backends.sqlite3', (default)
#            'django.db.backends.mysql',
#            'django.db.backends.postgresql_psycopg2' (see Issue 241),
#            'django.db.backends.oracle' (untested).
# NAME - database name, or path to the db file for sqlite3
# USER - db admin (unused in sqlite3)
# PASSWORD - db admin password (unused in sqlite3)
# HOST - empty string is localhost (unused in sqlite3)
# PORT - empty string defaults to localhost (unused in sqlite3)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(GAME_DIR, "server", "muddery.db3"),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': ''
        },
    'worlddata': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(GAME_DIR, "server", "worlddata.db3"),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': ''
        }}


# Database's router
DATABASE_ROUTERS = ['muddery.worlddata.db.database_router.DatabaseAppsRouter']

DATABASE_APPS_MAPPING = {
    'worlddata': 'worlddata',
}

######################################################################
# Evennia pluggable modules
######################################################################
# Plugin modules extend Evennia in various ways. In the cases with no
# existing default, there are examples of many of these modules
# in contrib/examples.

# The command parser module to use. See the default module for which
# functions it must implement
COMMAND_PARSER = "muddery.server.conf.cmdparser.cmdparser"

# The handler that outputs errors when using any API-level search
# (not manager methods). This function should correctly report errors
# both for command- and object-searches. This allows full control
# over the error output (it uses SEARCH_MULTIMATCH_TEMPLATE by default).
# SEARCH_AT_RESULT = "muddery.server.conf.at_search_result"

# An optional module that, if existing, must hold a function
# named at_initial_setup(). This hook method can be used to customize
# the server's initial setup sequence (the very first startup of the system).
# The check will fail quietly if module doesn't exist or fails to load.
AT_INITIAL_SETUP_HOOK_MODULE = "muddery.server.conf.at_initial_setup"

# Module containing your custom at_server_start(), at_server_reload() and
# at_server_stop() methods. These methods will be called every time
# the server starts, reloads and resets/stops respectively.
AT_SERVER_STARTSTOP_MODULE = "muddery.server.conf.at_server_startstop"

# List of one or more module paths to modules containing a function start_
# plugin_services(application). This module will be called with the main
# Evennia Server application when the Server is initiated.
# It will be called last in the startup sequence.
SERVER_SERVICES_PLUGIN_MODULES = ["muddery.server.conf.server_services_plugins"]

# List of one or more module paths to modules containing a function
# start_plugin_services(application). This module will be called with the
# main Evennia Portal application when the Portal is initiated.
# It will be called last in the startup sequence.
PORTAL_SERVICES_PLUGIN_MODULES = ["muddery.server.conf.portal_services_plugins"]

# Module holding MSSP meta data. This is used by MUD-crawlers to determine
# what type of game you are running, how many players you have etc.
MSSP_META_MODULE = "muddery.server.conf.mssp"

# Module for web plugins.
WEB_PLUGINS_MODULE = "muddery.server.conf.web_plugins"

# Tuple of modules implementing lock functions. All callable functions
# inside these modules will be available as lock functions.
LOCK_FUNC_MODULES = ("evennia.locks.lockfuncs", "muddery.server.conf.lockfuncs",)

# Module holding handlers for managing incoming data from the client. These
# will be loaded in order, meaning functions in later modules may overload
# previous ones if having the same name.
INPUT_FUNC_MODULES = ["evennia.server.inputfuncs", "muddery.server.conf.inputfuncs"]

# Modules that contain prototypes for use with the spawner mechanism.
PROTOTYPE_MODULES = ["muddery.world.prototypes"]


######################################################################
# Inlinefunc
######################################################################
# Evennia supports inline function preprocessing. This allows users
# to supply inline calls on the form $func(arg, arg, ...) to do
# session-aware text formatting and manipulation on the fly. If
# disabled, such inline functions will not be parsed.
INLINEFUNC_ENABLED = False
# Only functions defined globally (and not starting with '_') in
# these modules will be considered valid inlinefuncs. The list
# is loaded from left-to-right, same-named functions will overload
INLINEFUNC_MODULES = ["evennia.utils.inlinefuncs",
                      "muddery.server.conf.inlinefuncs"]


######################################################################
# Evennia base server config
######################################################################
# Activate telnet service
TELNET_ENABLED = False


######################################################################
# Django web features
######################################################################

# Context processors define context variables, generally for the template
# system to use.
TEMPLATE_CONTEXT_PROCESSORS = ('django.core.context_processors.i18n',
                               'django.core.context_processors.request',
                               'django.contrib.auth.context_processors.auth',
                               'django.core.context_processors.media',
                               'django.core.context_processors.debug',
                               'muddery.web.utils.general_context.general_context',)

# Absolute path to the directory that holds file uploads from web apps.
# Example: "/home/media/media.lawrence.com"
MEDIA_ROOT = os.path.join(GAME_DIR, "web", "media")

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = '/media/'

# resource's location
IMAGE_PATH = 'image'

# The master urlconf file that contains all of the sub-branches to the
# applications. Change this to add your own URLs to the website.
ROOT_URLCONF = 'web.urls'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure
# to use a trailing slash. Django1.4+ will look for admin files under
# STATIC_URL/admin.
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(GAME_DIR, "web", "static")

# URL that handles the webclient.
WEBCLIENT_ROOT = os.path.join(GAME_DIR, "web", "static", "webclient")

# URL that handles the worldeditor.
WORLDEDITOR_ROOT = os.path.join(GAME_DIR, "web", "static", "editor")

# Directories from which static files will be gathered from.
STATICFILES_DIRS = (
    os.path.join(GAME_DIR, "web", "static_overrides"),
    os.path.join(MUDDERY_DIR, "web", "website", "static"),
    ("webclient", os.path.join(GAME_DIR, "web", "webclient_overrides", "webclient")),
    ("webclient", os.path.join(MUDDERY_DIR, "web", "webclient", "webclient")),
    ("editor", os.path.join(GAME_DIR, "worlddata", "webclient")),
    ("editor", os.path.join(MUDDERY_DIR, "worlddata", "webclient")),
)

# We setup the location of the website template as well as the admin site.
TEMPLATES = [{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(GAME_DIR, "web", "template_overrides", WEBSITE_TEMPLATE),
            os.path.join(GAME_DIR, "web", "template_overrides"),
            os.path.join(MUDDERY_DIR, "web", "website", "templates", WEBSITE_TEMPLATE),
            os.path.join(MUDDERY_DIR, "web", "website", "templates"),
            os.path.join(EVENNIA_DIR, "web", "website", "templates", WEBSITE_TEMPLATE),
            os.path.join(EVENNIA_DIR, "web", "website", "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            "context_processors": [
                'django.template.context_processors.i18n',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.media',
                'django.template.context_processors.debug',
                'muddery.web.utils.general_context.general_context']
            }
        }]


######################################################################
# Typeclasses and other paths
######################################################################

# Server-side session class used.
SERVER_SESSION_CLASS = "muddery.server.conf.serversession.ServerSession"

# These are paths that will be prefixed to the paths given if the
# immediately entered path fail to find a typeclass. It allows for
# shorter input strings. They must either base off the game directory
# or start from the evennia library.
TYPECLASS_PATHS = ["muddery.typeclasses"]

# Typeclass for account objects (linked to a character) (fallback)
BASE_ACCOUNT_TYPECLASS = "muddery.typeclasses.accounts.MudderyAccount"

# Typeclass and base for all objects (fallback)
BASE_OBJECT_TYPECLASS = "muddery.typeclasses.object.MudderyBaseObject"

# Typeclass for character objects linked to a player (fallback)
BASE_CHARACTER_TYPECLASS = "muddery.typeclasses.player_character.MudderyPlayerCharacter"

# Typeclass for general characters, include NPCs, mobs and player characters.
BASE_GENERAL_CHARACTER_TYPECLASS = "muddery.typeclasses.character.MudderyCharacter"

# Typeclass for player characters.
BASE_PLAYER_CHARACTER_TYPECLASS = "muddery.typeclasses.player_character.MudderyPlayerCharacter"

# Typeclass for rooms (fallback)
BASE_ROOM_TYPECLASS = "muddery.typeclasses.room.MudderyRoom"

# Typeclass for Exit objects (fallback).
BASE_EXIT_TYPECLASS = "muddery.typeclasses.exit.MudderyExit"

# Typeclass for Channel (fallback).
BASE_CHANNEL_TYPECLASS = "muddery.typeclasses.channels.MudderyChannel"

# Typeclass for Scripts (fallback). You usually don't need to change this
# but create custom variations of scripts on a per-case basis instead.
BASE_SCRIPT_TYPECLASS = "muddery.typeclasses.scripts.MudderyScript"

# Path of base world data forms.
PATH_DATA_FORMS_BASE = "muddery.worlddata.forms"

# Path of base request processers.
PATH_REQUEST_PROCESSERS_BASE = "muddery.worlddata.controllers"

# Path of base typeclasses.
PATH_TYPECLASSES_BASE = "muddery.typeclasses"

# Path of custom typeclasses.
PATH_TYPECLASSES_CUSTOM = "typeclasses"

# Path of base event actions.
PATH_EVENT_ACTION_BASE = "muddery.events.event_actions"

# Path of base quest status.
PATH_QUEST_STATUS_BASE = "muddery.quests.quest_status"


######################################################################
# Default Player setup and access
######################################################################

# Different Multisession modes allow a player (=account) to connect to the
# game simultaneously with multiple clients (=sessions). In modes 0,1 there is
# only one character created to the same name as the account at first login.
# In modes 2,3 no default character will be created and the MAX_NR_CHARACTERS
# value (below) defines how many characters the default char_create command
# allow per player.
#  0 - single session, one player, one character, when a new session is
#      connected, the old one is disconnected
#  1 - multiple sessions, one player, one character, each session getting
#      the same data
#  2 - multiple sessions, one player, many characters, one session per
#      character (disconnects multiplets)
#  3 - like mode 2, except multiple sessions can puppet one character, each
#      session getting the same data.
MULTISESSION_MODE = 2

# The maximum number of characters allowed for MULTISESSION_MODE 2,3. This is
# checked by the default ooc char-creation command. Forced to 1 for
# MULTISESSION_MODE 0 and 1.
MAX_NR_CHARACTERS = 3


######################################################################
# Default statement sets
######################################################################

# Action functions set
ACTION_FUNC_SET = "muddery.statements.default_statement_func_set.ActionFuncSet"

# Condition functions set
CONDITION_FUNC_SET = "muddery.statements.default_statement_func_set.ConditionFuncSet"

# Skill functions set
SKILL_FUNC_SET = "muddery.statements.default_statement_func_set.SkillFuncSet"


######################################################################
# Default command sets
######################################################################

# Command set used on session before player has logged in
CMDSET_UNLOGGEDIN = "muddery.commands.default_cmdsets.UnloggedinCmdSet"

# Command set used on the logged-in session
CMDSET_SESSION = "muddery.commands.default_cmdsets.SessionCmdSet"

# Default set for logged in player with characters (fallback)
CMDSET_CHARACTER = "muddery.commands.default_cmdsets.CharacterCmdSet"

# Command set for accounts without a character (ooc)
CMDSET_ACCOUNT = "muddery.commands.default_cmdsets.AccountCmdSet"

# Command set for players in combat
CMDSET_COMBAT = "muddery.commands.default_cmdsets.CombatCmdSet"


######################################################################
# Muddery additional data features
######################################################################
# data app name
ADDITIONAL_DATA_APP = "database"

# add data app
INSTALLED_APPS = INSTALLED_APPS + (ADDITIONAL_DATA_APP,)


######################################################################
# World data features
######################################################################

# attribute's category for data info
DATA_KEY_CATEGORY = "data_key"

# data app name
WORLD_DATA_APP = "worlddata"

# add data app
INSTALLED_APPS = INSTALLED_APPS + (WORLD_DATA_APP,)

# data file's folder under user's game directory.
WORLD_DATA_FOLDER = os.path.join("worlddata", "data")

# Character's typeclass key.
GENERAL_CHARACTER_TYPECLASS_KEY = "CHARACTER"

# Localized string data's folder.
LOCALIZED_STRINGS_FOLDER = "languages"

# Localized string model's name
LOCALIZED_STRINGS_MODEL = "localized_strings"

# World data API's url path.
WORLD_DATA_API_PATH = "worlddata/editor/api"


###################################
# permissions
###################################
# Characters who have these permission can bypass events.
PERMISSION_BYPASS_EVENTS = {"builders", "wizards", "immortals"}

# Characters who have these permission can use text commands.
PERMISSION_COMMANDS = {"playerhelpers", "builders", "wizards", "immortals"}


###################################
# world editor
###################################
DEFUALT_LIST_TEMPLATE = "common_list.html"

DEFUALT_FORM_TEMPLATE = "common_form.html"


###################################
# combat settings
###################################
# Handler of the combat
NORMAL_COMBAT_HANDLER = "muddery.combat.normal_combat_handler.NormalCombatHandler"

HONOUR_COMBAT_HANDLER = "muddery.combat.honour_auto_combat_handler.HonourAutoCombatHandler"

AUTO_COMBAT_TIMEOUT = 60


###################################
# honour settings
###################################
MIN_HONOUR_LEVEL = 2

TOP_RANKINGS_NUMBER = 10

NEAREST_RANKINGS_NUMBER = 10

HONOUR_OPPONENTS_NUMBER = 100


###################################
# AI modules
###################################
AI_CHOOSE_SKILL = "muddery.ai.choose_skill.ChooseSkill"

