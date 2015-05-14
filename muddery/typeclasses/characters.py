"""
Characters

Characters are (by default) Objects setup to be puppeted by Players.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""

from muddery.typeclasses.objects import MudderyObject
from evennia.objects.objects import DefaultCharacter

class MudderyCharacter(MudderyObject, DefaultCharacter):
    """
    The Character defaults to implementing some of its hook methods with the
    following standard functionality:

    at_basetype_setup - always assigns the DefaultCmdSet to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead)
    at_after_move - launches the "look" command
    at_post_puppet(player) -  when Player disconnects from the Character, we
                    store the current location, so the "unconnected" character
                    object does not need to stay on grid but can be given a
                    None-location while offline.
    at_pre_puppet - just before Player re-connects, retrieves the character's
                    old location and puts it back on the grid with a "charname
                    has connected" message echoed to the room

    """
    def at_object_creation(self):
        """
        Called once, when this object is first created. This is the
        normal hook to overload for most object types.
            
        """
        super(MudderyCharacter, self).at_object_creation()

        # add default hp
        self.db.hp = 100


    def at_object_receive(self, moved_obj, source_location):
        """
        Called after an object has been moved into this object.
        
        Args:
        moved_obj (Object): The object moved into this one
        source_location (Object): Where `moved_object` came from.
        
        """
        super(MudderyCharacter, self).at_object_receive(moved_obj, source_location)

        # send latest inventory data to player
        inv = self.return_inventory()
        self.msg({"inventory":inv})
    
        
    def at_object_left(self, moved_obj, target_location):
        """
        Called after an object has been removed from this object.
        
        Args:
        moved_obj (Object): The object leaving
        target_location (Object): Where `moved_obj` is going.
        
        """
        super(MudderyCharacter, self).at_object_left(moved_obj, target_location)
        
        # send latest inventory data to player
        inv = self.return_inventory()
        self.msg({"inventory":inv})


    def at_after_move(self, source_location):
        """
        We make sure to look around after a move.

        """
        self.msg({"msg": "Moving to %s ..." % self.location.name})

        if self.location:
            appearance = self.location.get_appearance(self)
            appearance.update(self.location.get_surroundings(self))
            self.msg({"look_around":appearance})


    def at_post_puppet(self):
        """
        Called just after puppeting has been completed and all
        Player<->Object links have been established.

        """
        super(MudderyCharacter, self).at_post_puppet()

        # send status to player
        status = self.return_status()
        self.msg({"status": status})
        
        # send inventory data to player
        inv = self.return_inventory()
        self.msg({"inventory": inv})


    def return_inventory(self):
        """
        Get inventory's data.
        """
        inv = []
        items = self.contents
        for item in items:
            inv.append({"dbref": item.dbref,
                        "name": item.name,
                        "desc": item.db.desc})
        return inv

    def return_status(self):
        """
        Get character's status.
        """
        status = {"hp": self.db.hp}
        
        return status