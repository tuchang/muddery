"""
DialogueHandler

The DialogueHandler maintains a pool of dialogues.

"""

from __future__ import print_function

import re
from muddery.utils import defines
from muddery.statements.statement_handler import STATEMENT_HANDLER
from muddery.utils.game_settings import GAME_SETTINGS
from muddery.mappings.event_action_set import EVENT_ACTION_SET
from muddery.worlddata.dao.dialogues_mapper import DIALOGUES
from muddery.worlddata.dao.dialogue_sentences_mapper import DIALOGUE_SENTENCES
from muddery.worlddata.dao.npc_dialogues_mapper import NPC_DIALOGUES
from muddery.mappings.quest_status_set import QUEST_STATUS_SET
from muddery.worlddata.dao.event_mapper import EVENTS
from muddery.events.event_trigger import EventTrigger
from evennia.utils import logger


class DialogueHandler(object):
    """
    The DialogueHandler maintains a pool of dialogues.
    """
    speaker_escape = re.compile(r'%[%|p|n]')

    @staticmethod
    def escape_fun(word):
        """
        Change escapes to target words.
        """
        escape_word = word.group()
        char = escape_word[1]
        if char == "%":
            return char
        else:
            return "%(" + char + ")s"

    def get_npc_sentences(self, caller, npc):
        """
        Get NPC's sentences that can show to the caller.

        Args:
            caller: (object) the character who want to start a talk.
            npc: (object) the NPC that the character want to talk to.

        Returns:
            sentences: (list) a list of available sentences.
        """
        if not caller:
            return

        if not npc:
            return

        # all sentences
        sentences = []

        # Get NPC's dialogues.
        for dlg_key in npc.dialogues:
            # Get dialogue's sentences.
            dialogue = DIALOGUES.get(dlg_key)

            # added sentence's key
            added = set()
            sentences.extend(self.get_sentences(dialogue.sentence, caller, npc, added))

        return sentences

    def get_sentences(self, sentence_key, caller, npc, added):
        """
        Get a dialogue's sentences that can show to the caller.

        Args:
            sentence_key: (string) a dialogue's key.
            caller: (object) the character who want to start a talk.
            npc: (object) the NPC that the character want to talk to.
            added: (set) sentences that has already added.

        Returns:
            sentences: (list) a list of available sentences.
        """
        sentences = []

        record = DIALOGUE_SENTENCES.get(sentence_key)
        if not STATEMENT_HANDLER.match_condition(record.condition, caller, npc):
            # if not match condition
            return sentences

        # add this sentence
        sentences.append(self.get_output(record, caller, npc))
        added.add(record.key)

        # check events
        if EVENTS.has_event(sentence_key):
            # If this sentence has events, it must notify the server to continue.
            return sentences

        # add nexts
        next_sentences = record.nexts.split(",")
        for next_sentence in next_sentences:
            if next_sentence in added:
                continue

            sentences.extend(self.get_sentences(next, caller, npc, added))

        return sentences

    def get_dialogue_speaker_name(self, caller, npc, speaker_model):
        """
        Get the speaker's text.
        'p' means player.
        'n' means NPC.
        Use string in quotes directly.
        """
        caller_name = ""
        npc_name = ""

        if caller:
            caller_name = caller.get_name()
        if npc:
            npc_name = npc.get_name()

        values = {"p": caller_name,
                  "n": npc_name}
        speaker = speaker_model % values

        return speaker

    def get_dialogue_speaker_icon(self, icon_str, caller, npc, speaker_model):
        """
        Get the speaker's text.
        'p' means player.
        'n' means NPC.
        Use string in quotes directly.
        """
        icon = None

        # use icon resource in dialogue sentence
        if icon_str:
            icon = icon_str
        else:
            if "%(n)" in speaker_model:
                if npc:
                    icon = getattr(npc, "icon", None)
            elif "%(p)" in speaker_model:
                icon = getattr(caller, "icon", None)

        return icon

    def get_output(self, record, caller, npc):
        """
        Create a sentence of an output format.

        Args:
            record: (record) sentence's data
            caller: (object) caller object
            npc: (object, optional) NPC object

        Returns:
            (dict) a sentence's data
        """
        speaker_model = self.speaker_escape.sub(self.escape_fun, record.speaker)
        speaker = self.get_dialogue_speaker_name(caller, npc, speaker_model)
        icon = self.get_dialogue_speaker_icon(record.icon, caller, npc, speaker_model)

        sentence = {"speaker": speaker,                 # speaker's name
                    "sentence": record.key,             # sentence's key
                    "nexts": record.nexts.split(","),   # this sentence's next sentences
                    "content": record.content,
                    "icon": icon}
        if npc:
            sentence["npc"] = npc.dbref             # NPC's dbref
        else:
            sentence["npc"] = ""

        return sentence

    def finish_sentence(self, sentence_key, caller, npc):
        """
        A sentence finished, do it's event.
        """
        if not caller:
            return
        
        # get dialogue
        dlg = self.get_dialogue(dialogue)
        if not dlg:
            return

        if sentence_no >= len(dlg["sentences"]):
            return

        sentence = self.get_sentence(dialogue, sentence_no)
        if not sentence:
            return

        # do dialogue's event
        if sentence["event"]:
            sentence["event"].at_sentence(caller, npc)

        if sentence["is_last"]:
            # last sentence
            self.finish_dialogue(caller, dialogue)

    def finish_dialogue(self, caller, npc, dialogue):
        """
        A dialogue finished, do it's action.
        args:
            caller(object): the dialogue caller
            dialogue(string): dialogue's key
        """
        if not caller:
            return

        # trigger dialogue's event
        if self.dialogue_storage["event"]:
            self.dialogue_storage["event"].at_sentence(caller, npc)


        caller.quest_handler.at_objective(defines.OBJECTIVE_TALK, dialogue)

    def have_quest(self, caller, npc):
        """
        Check if the npc can provide or finish quests.
        Completing is higher than providing.
        """
        provide_quest = False
        finish_quest = False

        if not caller:
            return (provide_quest, finish_quest)

        if not npc:
            return (provide_quest, finish_quest)

        # get npc's default dialogues
        for dlg_key in npc.dialogues:
            # find quests by recursion
            provide, finish = self.dialogue_have_quest(caller, npc, dlg_key)
                
            provide_quest = (provide_quest or provide)
            finish_quest = (finish_quest or finish)

            if finish_quest:
                break

            if not caller.quest_handler.get_accomplished_quests():
                if provide_quest:
                    break

        return (provide_quest, finish_quest)

    def dialogue_have_quest(self, caller, npc, dialogue):
        """
        Find quests by recursion.
        """
        provide_quest = False
        finish_quest = False

        # check if the dialogue is available
        npc_dlg = self.get_dialogue(dialogue)
        if not npc_dlg:
            return (provide_quest, finish_quest)

        if not STATEMENT_HANDLER.match_condition(npc_dlg["condition"], caller, npc):
            return (provide_quest, finish_quest)

        match = True
        for dep in npc_dlg["dependencies"]:
            status = QUEST_STATUS_SET.get(dep["type"])
            if not status.match(caller, dep["quest"]):
                match = False
                break
        if not match:
            return (provide_quest, finish_quest)

        # find quests in its sentences
        for sen in npc_dlg["sentences"]:
            for quest_key in sen["finish_quest"]:
                if caller.quest_handler.is_accomplished(quest_key):
                    finish_quest = True
                    return (provide_quest, finish_quest)

            if not provide_quest and sen["provide_quest"]:
                for quest_key in sen["provide_quest"]:
                    if caller.quest_handler.can_provide(quest_key):
                        provide_quest = True
                        return (provide_quest, finish_quest)

        for dlg_key in npc_dlg["nexts"]:
            # get next dialogue
            provide, finish = self.dialogue_have_quest(caller, npc, dlg_key)
                
            provide_quest = (provide_quest or provide)
            finish_quest = (finish_quest or finish)

            if finish_quest:
                break

            if not caller.quest_handler.get_accomplished_quests():
                if provide_quest:
                    break

        return (provide_quest, finish_quest)


# main dialoguehandler
DIALOGUE_HANDLER = DialogueHandler()
