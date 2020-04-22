import curses
import os
from curses.textpad import Textbox
from .utils import mkculor


class Action:
    def __init__(self, stdscr, lines):
        self.stdscr = stdscr
        self.lines = lines
        self.maxy, self.maxx = self.stdscr.getmaxyx()
        self.longest = len(max(self.lines, key=len))
        self.foot = curses.newwin(0, self.maxx, self.maxy - 1, 0)
        self.pad = curses.newpad(len(self.lines) + 1, self.longest + 1)
        self.pad.keypad(True)  # use function keys
        self.pad.idlok(True)
        self.pad.scrollok(True)
        self.pminrow = 0  # pad row to start displaying contents at
        self.pmincol = 0  # pad column to start displaying contents at
        self.matches = []
        self.color = mkculor()
        curses.curs_set(0)  # hide the cursor

    def up(self):
        if self.pminrow > 0:
            self.pminrow -= 1

    def down(self):
        if self.pminrow < len(self.lines) - self.maxy:
            self.pminrow += 1

    def left(self):
        if self.pmincol > 0:
            self.pmincol -= 1

    def right(self):
        if self.pmincol < self.longest - self.maxx:
            self.pmincol += 1

    def pgup(self):
        if self.pminrow > 0:
            self.pminrow -= self.maxy

    def pgdn(self):
        if self.pminrow < len(self.lines) - self.maxy:
            self.pminrow += self.maxy
        if self.pminrow > len(self.lines) - self.maxy:
            self.pminrow = len(self.lines) - self.maxy

    def top(self):
        self.pminrow = 0

    def bottom(self):
        self.pminrow = len(self.lines) - self.maxy

    def next(self):
        if self.matches:
            for i in self.matches:
                if self.pminrow < i:
                    self.pminrow = i
                    return

            self.top()
            self.next()

    def prev(self):
        if self.matches:
            for i in reversed(self.matches):
                if self.pminrow > i:
                    self.pminrow = i
                    return

            self.bottom()
            self.prev()

    def _match(self, msg):
        search = self._textbox(msg).strip()

        if not search:
            return

        for index, line in enumerate(self.lines):
            if search in line:
                if index not in self.matches:
                    self.matches.append(index)

        if self.matches:
            self.next()

    def find(self):
        self.matches = []
        self._match("Find: ")

    def reset(self):
        self.matches = []

    def refresh(self):
        self.stdscr.noutrefresh()
        self.pad.noutrefresh(
            self.pminrow, self.pmincol, 0, 0, self.maxy - 2, self.maxx - 1
        )
        self.foot.noutrefresh()
        curses.doupdate()

    def resize(self):
        self.stdscr.erase()
        self.pad.erase()
        self.maxy, self.maxx = self.stdscr.getmaxyx()
        self.foot.mvwin(self.maxy - 1, 0)
        self.foot.resize(1, self.maxx)

    def draw_footer(self, msg):
        try:
            self.foot.addstr(0, 0, msg, self.color["blue_white_bold"])
            self.foot.bkgdset(self.color["blue_white_bold"])
            self.foot.clrtoeol()  # more frugal than erase. no flicker.
        except curses.error:
            pass

    def _textbox(self, prompt):
        self.foot.erase()
        self.foot.addstr(0, 0, prompt, curses.A_BOLD)
        curses.curs_set(1)
        self.foot.refresh()
        tb = self.foot.subwin(self.maxy - 1, len(prompt))
        box = Textbox(tb)
        box.edit()
        curses.curs_set(0)
        result = box.gather()
        self.foot.erase()
        return result

    def save(self):
        path = self._textbox("Save to: ").strip()
        path = os.path.abspath(os.path.expanduser(path))
        out = None
        try:
            # removes need to use f.close
            with open(path, "a+") as f:
                for line in self.lines:
                    f.write(line)
        except FileNotFoundError:
            out = "Can't find " + path
        except IsADirectoryError:
            out = path + " is a directory."
        except UnboundLocalError:  # bit of a hack but fuck it
            out = "Not saving items."
        except Exception:
            out = "Something went wrong..."
        else:
            out = "Saved items to " + path
        finally:
            return out

    def quit(self):
        return "quit"
