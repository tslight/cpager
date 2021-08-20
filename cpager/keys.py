import curses
from .action import Action
from os import environ

environ.setdefault("ESCDELAY", "12")  # otherwise it takes an age!


class Keys(Action):
    """
    Translate keys to actions.
    """

    def __init__(self, stdscr, lines):
        super().__init__(stdscr, lines)
        self.help = [
            "[h][LEFT]     : Scroll left one character.",
            "[l][RIGHT]    : Scroll right one column.",
            "[k][UP]       : Scroll up one line.",
            "[j][DOWN]     : Scroll down one line.",
            "[f][PGDN]     : Scroll down a page of lines.",
            "[b][PGUP]     : Scroll up a page of lines.",
            "[g][HOME]     : Go to first page.",
            "[G][END]      : Go to last page.",
            "[/]           : Search via wildcards or regex.",
            "[n]           : Jump to next search result.",
            "[p]           : Jump to previous search result.",
            "[r]           : Reset search results.",
            "[?][F1]       : View this help page.",
            "[w][CTRL-s]   : Save contents to file.",
            "[q][ESC]      : Quit and exit.",
        ]

        # The keys in this dictionary map onto methods in the Action class.
        self.keys = {
            "resize": [curses.KEY_RESIZE],
            "left": [ord("h"), curses.KEY_LEFT],
            "right": [ord("l"), curses.KEY_RIGHT],
            "down": [ord("j"), curses.KEY_DOWN],
            "up": [ord("k"), curses.KEY_UP],
            "pgdn": [ord("f"), curses.KEY_NPAGE],
            "pgup": [ord("b"), curses.KEY_PPAGE],
            "top": [ord("g"), curses.KEY_HOME],
            "bottom": [ord("G"), curses.KEY_END],
            "find": [ord("/")],
            "next": [ord("n")],
            "prev": [ord("p")],
            "reset": [ord("r")],
            "show_help": [ord("?"), curses.KEY_F1],
            "save": [ord("w"), curses.ascii.ctrl(ord("s"))],
            "quit": [ord("q"), curses.ascii.ESC],
        }

    def show_help(self):
        pminrow, pmincol = self.pminrow, self.pmincol
        self.pminrow, self.pmincol = (0,) * 2
        self.pad.erase()
        while True:
            self.draw_footer("Press [q] or [ESC] to return to pager.")
            for idx, line in enumerate(self.help):
                self.pad.addstr(idx, 0, line)

            self.refresh()

            key = self.stdscr.getch()
            if self.action(key) == "quit":
                break

        self.pminrow, self.pmincol = pminrow, pmincol

    def action(self, key):
        """
        Run a key from the keys dictionary as a method.
        """
        try:
            action = [k for (k, v) in self.keys.items() if key in v][0]
            return getattr(self, action)()
        except IndexError:
            pass
