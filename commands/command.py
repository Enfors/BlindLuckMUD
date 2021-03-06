"""
Commands

Commands describe the input the account can do to the game.

"""

import random

from evennia.commands.command import Command as BaseCommand

from evennia import create_object

# from evennia import default_cmds


class Command(BaseCommand):
    """
    Inherit from this if you want to create your own command styles
    from scratch.  Note that Evennia's default commands inherits from
    MuxCommand instead.

    Note that the class's `__doc__` string (this text) is
    used by Evennia to create the automatic help entry for
    the command, so make sure to document consistently here.

    Each Command implements the following methods, called
    in this order (only func() is actually required):
        - at_pre_cmd(): If this returns anything truthy, execution is aborted.
        - parse(): Should perform any extra parsing needed on self.args
            and store the result on self.
        - func(): Performs the actual work.
        - at_post_cmd(): Extra actions, often things done after
            every command, like prompts.

    """

    pass


# -------------------------------------------------------------
#
# The default commands inherit from
#
#   evennia.commands.default.muxcommand.MuxCommand.
#
# If you want to make sweeping changes to default commands you can
# uncomment this copy of the MuxCommand parent and add
#
#   COMMAND_DEFAULT_CLASS = "commands.command.MuxCommand"
#
# to your settings file. Be warned that the default commands expect
# the functionality implemented in the parse() method, so be
# careful with what you change.
#
# -------------------------------------------------------------

# from evennia.utils import utils
#
#
# class MuxCommand(Command):
#     """
#     This sets up the basis for a MUX command. The idea
#     is that most other Mux-related commands should just
#     inherit from this and don't have to implement much
#     parsing of their own unless they do something particularly
#     advanced.
#
#     Note that the class's __doc__ string (this text) is
#     used by Evennia to create the automatic help entry for
#     the command, so make sure to document consistently here.
#     """
#     def has_perm(self, srcobj):
#         """
#         This is called by the cmdhandler to determine
#         if srcobj is allowed to execute this command.
#         We just show it here for completeness - we
#         are satisfied using the default check in Command.
#         """
#         return super().has_perm(srcobj)
#
#     def at_pre_cmd(self):
#         """
#         This hook is called before self.parse() on all commands
#         """
#         pass
#
#     def at_post_cmd(self):
#         """
#         This hook is called after the command has finished executing
#         (after self.func()).
#         """
#         pass
#
#     def parse(self):
#         """
#         This method is called by the cmdhandler once the command name
#         has been identified. It creates a new set of member variables
#         that can be later accessed from self.func() (see below)
#
#         The following variables are available for our use when entering this
#         method (from the command definition, and assigned on the fly by the
#         cmdhandler):
#            self.key - the name of this command ('look')
#            self.aliases - the aliases of this cmd ('l')
#            self.permissions - permission string for this command
#            self.help_category - overall category of command
#
#            self.caller - the object calling this command
#            self.cmdstring - the actual command name used to call this
#                             (this allows you to know which alias was used,
#                              for example)
#            self.args - the raw input; everything following self.cmdstring.
#            self.cmdset - the cmdset from which this command was picked. Not
#                          often used (useful for commands like 'help' or to
#                          list all available commands etc)
#            self.obj - the object on which this command was defined. It is often
#                          the same as self.caller.
#
#         A MUX command has the following possible syntax:
#
#           name[ with several words][/switch[/switch..]] arg1[,arg2,...] [[=|,] arg[,..]]
#
#         The 'name[ with several words]' part is already dealt with by the
#         cmdhandler at this point, and stored in self.cmdname (we don't use
#         it here). The rest of the command is stored in self.args, which can
#         start with the switch indicator /.
#
#         This parser breaks self.args into its constituents and stores them in the
#         following variables:
#           self.switches = [list of /switches (without the /)]
#           self.raw = This is the raw argument input, including switches
#           self.args = This is re-defined to be everything *except* the switches
#           self.lhs = Everything to the left of = (lhs:'left-hand side'). If
#                      no = is found, this is identical to self.args.
#           self.rhs: Everything to the right of = (rhs:'right-hand side').
#                     If no '=' is found, this is None.
#           self.lhslist - [self.lhs split into a list by comma]
#           self.rhslist - [list of self.rhs split into a list by comma]
#           self.arglist = [list of space-separated args (stripped, including '=' if it exists)]
#
#           All args and list members are stripped of excess whitespace around the
#           strings, but case is preserved.
#         """
#         raw = self.args
#         args = raw.strip()
#
#         # split out switches
#         switches = []
#         if args and len(args) > 1 and args[0] == "/":
#             # we have a switch, or a set of switches. These end with a space.
#             switches = args[1:].split(None, 1)
#             if len(switches) > 1:
#                 switches, args = switches
#                 switches = switches.split('/')
#             else:
#                 args = ""
#                 switches = switches[0].split('/')
#         arglist = [arg.strip() for arg in args.split()]
#
#         # check for arg1, arg2, ... = argA, argB, ... constructs
#         lhs, rhs = args, None
#         lhslist, rhslist = [arg.strip() for arg in args.split(',')], []
#         if args and '=' in args:
#             lhs, rhs = [arg.strip() for arg in args.split('=', 1)]
#             lhslist = [arg.strip() for arg in lhs.split(',')]
#             rhslist = [arg.strip() for arg in rhs.split(',')]
#
#         # save to object properties:
#         self.raw = raw
#         self.switches = switches
#         self.args = args.strip()
#         self.arglist = arglist
#         self.lhs = lhs
#         self.lhslist = lhslist
#         self.rhs = rhs
#         self.rhslist = rhslist
#
#         # if the class has the account_caller property set on itself, we make
#         # sure that self.caller is always the account if possible. We also create
#         # a special property "character" for the puppeted object, if any. This
#         # is convenient for commands defined on the Account only.
#         if hasattr(self, "account_caller") and self.account_caller:
#             if utils.inherits_from(self.caller, "evennia.objects.objects.DefaultObject"):
#                 # caller is an Object/Character
#                 self.character = self.caller
#                 self.caller = self.caller.account
#             elif utils.inherits_from(self.caller, "evennia.accounts.accounts.DefaultAccount"):
#                 # caller was already an Account
#                 self.character = self.caller.get_puppet(self.session)
#             else:
#                 self.character = None

class CmdKill(Command):
    """
    Attack another character.

    Usage:
      kill (character name)
    """
    key = "kill"
    aliases = []
    lock = "cmd:all()"
    help_category = "Combat"

    def func(self):
        "Attempts to kill another character."

        caller = self.caller

        if not self.args:
            caller.msg("Usage: kill <who>")
            return

        target_name = self.args.strip()

        target = caller.location.search(target_name)

        if not target:
            caller.msg(f"You don't see any {target_name} here.")
            return

        combat_result = random.randint(0, 1)

        if combat_result == 1:
            winner = caller
            loser = target
        else:
            winner = target
            loser = caller

        winner.msg(f"You have defeated {loser.key}!")
        loser.msg(f"You have been defeated by {winner.key}!")
        caller.location.msg_contents(f"{winner.key} has defeated {loser.key}!",
                                     exclude=[winner, loser])
        exp = 300
        winner.receive_exp(exp)


class CmdLevel(Command):
    """
    Show which level your character is.

    Usage:
      level
    """
    key = "level"
    aliases = []
    lock = "cmd:all()"
    help_category = "General"

    def func(self):
        caller = self.caller
        level = caller.get_level()
        caller.msg(f"You are level {level}.")

        exp = caller.get_total_exp()
        cost = caller.get_level_cost(level + 1)
        caller.msg(f"You have {exp} experience points, "
                   f"and need another {cost-exp} for next level.")

        unused_pts = caller.get_unused_stat_pts()
        if unused_pts == 1:
            pts_form = "point"
        else:
            pts_form = "points"

        if unused_pts == 0:
            unused_pts = "no"

        for stat in caller.stats:
            long_stat = caller.stats_long[stat].capitalize()
            stat_val = caller.get_stat(stat)
            caller.msg(f"{long_stat:12}: {stat_val:2}")

        caller.msg(f"You have {unused_pts} unused stat increase {pts_form}.")


class CmdIncrease(Command):
    """
    Increase one of your stats. Valid stats are:

    Intelligence
    Charisma
    Constitution
    Strength
    Dexterity
    Perception
    Wisdom

    Each time you get a level, you get five stat increase points.
    To show how much it costs to raise a stat, type:

      increase

    To increase a stat, type:

      increase (stat)

    For example:

      increase wisdom
    """
    key = "increase"
    aliases = ["inc"]
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        caller = self.caller

        args = self.args

        if not args:
            self.show_costs(caller)
        else:
            self.inc_stat(caller, self.args.strip())

    def show_costs(self, caller):
        stats = caller.stats

        caller.msg("The costs to increase your stats are as follows:")

        for stat in stats:
            cost = caller.get_inc_stat_cost(stat)
            stats_long = caller.stats_long[stat]
            caller.msg(f"{stats_long.capitalize():12}: {cost:2}")

        unused_pts = caller.get_unused_stat_pts()

        if unused_pts == 1:
            pts_form = "point"
        else:
            pts_form = "points"

        if unused_pts == 0:
            unused_pts = "no"

        caller.msg(f"You have {unused_pts} unused stat increase {pts_form} to increase your stats with.")

    def inc_stat(self, caller, stat):
        orig_stat = stat.lower()
        stat = stat.lower()[:3]
        stat_long = caller.stats_long[stat]  # Get "strength" from "str", etc.

        if stat not in caller.stats:
            caller.msg(f"{orig_stat.capitalize()} is not a valid stat.")
            return False

        if caller.inc_stat(stat):
            new_val = caller.get_stat(stat)
            caller.msg(f"Your {stat_long} has been increased to {new_val}.")
        else:
            caller.msg("Unfortunately, you do not have enough stat increase points to do that.")


class CmdCreateNPC(Command):
    """
    Create a new NPC (non-player character).

    Usage:
      +createNPC <name>

    Creates a new, named NPC.
    """
    key = "+createnpc"
    aliases = ["createNPC"]
    locks = "call:not perm(nonpcs)"
    help_category = "wizard"

    def func(self):
        """
        Creates the object and names it.
        """
        caller = self.caller

        if not self.args:
            caller.msg("Usage: +createNPC <name>")
            return
        if not caller.location:
            # May not create an NPC when OOC
            caller.msg("You must have a location to create an NPC.")
            return
        # Make the name always start with capital letter
        name = self.args.strip().capitalize()
        # Create an NPC in caller's location
        npc = create_object("characters.Character",
                            key=name,
                            location=caller.location,
                            locks=f"edit:id({caller.id}) and perm(Builders);call:false()")
        # Announce
        message = "%s created the NPC '%s'."
        caller.msg(message % ("You", name))
        caller.location.msg_contents(message % (caller.key, name),
                                     exclude=caller)
