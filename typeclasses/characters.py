"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
from evennia import DefaultCharacter


class Character(DefaultCharacter):
    """
    The Character defaults to reimplementing some of base Object's hook methods with the
    following functionality:

    at_basetype_setup - always assigns the DefaultCmdSet to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead).
    at_after_move(source_location) - Launches the "look" command after every move.
    at_post_unpuppet(account) -  when Account disconnects from the Character, we
                    store the current location in the pre_logout_location Attribute and
                    move it to a None-location so the "unpuppeted" character
                    object does not need to stay on grid. Echoes "Account has disconnected"
                    to the room.
    at_pre_puppet - Just before Account re-connects, retrieves the character's
                    pre_logout_location Attribute and move it back on the grid.
    at_post_puppet - Echoes "AccountName has entered the game" to the room.

    """

    stats = [
        "int",
        "cha",
        "con",
        "str",
        "dex",
        "per",
        "wis"
    ]

    stats_long = {
        "int": "intelligence",
        "cha": "charisma",
        "con": "constitution",
        "str": "strength",
        "dex": "dexterity",
        "per": "perception",
        "wis": "wisdom"
    }

    def at_object_creation(self):
        """
        This is called when the object is first created, only.
        """
        self.db.total_exp = 0
        self.db.used_stat_pts = 0  # Total num stat pts used

        # Set up starting stats
        starting_stats = dict()
        for stat in self.stats:
            starting_stats[stat] = 8
        self.attributes.add("starting_stats", starting_stats)

        # Set up stat incs
        stat_incs = dict()
        for stat in self.stats:
            stat_incs[stat] = 0

        self.attributes.add("stat_incs", stat_incs)

    # EXP FUNCTIONS

    def receive_exp(self, exp: int):
        """
        Give this character experience points.
        If this may increase the character's level.
        """
        if exp == 0:
            return self.get_total_exp()

        if exp < 0:
            pass

        old_level = self.get_level()

        self.db.total_exp += exp
        self.msg(f"You receive {exp} experience points.")

        new_level = self.get_level()

        if new_level > old_level:
            self.msg(f"|gCongratulations, you are now level {new_level}!")

    def set_total_exp(self, exp: int):
        """
        Set the character's total exp.
        """
        if exp < 0:
            exp = 0

        self.db.total_exp = exp
        return exp

    def get_total_exp(self):
        """
        Return the character's total exp.
        """
        return self.db.total_exp

    # LEVEL FUNCTIONS

    def get_level(self):
        """
        Calculate and return the character's level.
        """
        level = 0

        exp = self.db.total_exp

        while self.get_level_cost(level + 1) <= exp:
            level += 1

        return level

    def get_level_cost(self, level: int):
        """
        Return the total exp cost of a level.
        """

        if level < 0:
            return 0

        cur_level = 0
        cost = 500

        while cur_level < level:
            cur_level += 1
            if cur_level < level:
                cost += int(cost * .15) + 500

        cost = int((cost + 50) / 100) * 100

        return cost

    # STAT FUNCTIONS

    def get_starting_stat(self, stat: str):
        """
        Get a character's starting stat, the one the character started the game with.
        """
        if stat not in self.stats:
            # Todo: raise exception
            return None

        return self.db.starting_stats[stat]

    def get_stat(self, stat: str):
        """
        Get a character's stat, including any and all bonuses and increases they
        have made to their character.
        """
        if stat not in self.stats:
            # Todo: raise exception
            return None

        # Eventually, we will also have to add stat BONUSES here.
        return self.get_starting_stat(stat) + self.get_stat_incs(stat)

    def get_stat_incs(self, stat: str):
        """
        Return how many times the player has increased a stat.
        """
        if stat not in self.stats:
            # Todo: raise exception
            return None

        return self.db.stat_incs[stat]

    # STAT POINT FUNCTIONS

    def get_used_stat_pts(self):
        """
        Return the number of stat increase points that the character has used.
        """
        return self.db.used_stat_pts

    def get_unused_stat_pts(self):
        """
        Return the number of stat increase points that the character has yet
        to use.
        """
        total = self.get_total_stat_pts_for_level()
        used = self.get_used_stat_pts()

        unused = total - used

        if unused < 0:
            unused = 0

        return unused

    def get_total_stat_pts_for_level(self, level: int = None):
        """
        Get the total number of stat increase points that a character should
        have amassed at a certain level. If no level is provided, the character's
        current level is assumed.
        """

        if level is None:
            level = self.get_level()

        return level * 5

    def inc_stat(self, stat: str):
        """
        Called when the user wants to increase a stat by one point.
        If there are enough unused stat inc points, then the stat is increased
        and True is returned. Otherwise, False is returned.
        """

        if stat not in self.stats:
            # Todo: raise exception
            return None

        unused_pts = self.get_unused_stat_pts()
        cost = self.get_inc_stat_cost(stat)

        if cost > unused_pts:
            return False

        self.db.used_stat_pts += cost
        self.db.stat_incs[stat] += 1
        return True

    def get_inc_stat_cost(self, stat: str):
        """
        Returns how many stat inc pts it costs to increase stat.
        """

        if stat not in self.stats:
            # Todo: raise exception
            return None

        return self.db.stat_incs[stat] + 1

    # OTHER FUNCTIONS

    def die(self):
        """
        Called when a character dies.
        """
        # Todo: log here. This function shouldn't be called, it should be overridden.
        pass


class PlayerCharacter(Character):
    pass


class NonPlayerCharacter(Character):
    pass


class WizardCharacter(PlayerCharacter):
    pass
