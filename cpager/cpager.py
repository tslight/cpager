import curses
import curses.ascii
import re
import os

from argparse import ArgumentParser, ArgumentTypeError
from cansi import Cansi
from .keys import Keys

os.environ.setdefault("ESCDELAY", "12")  # otherwise it takes an age!


def chkinput(input):
    if os.path.isfile(os.path.expanduser(input)):
        path = os.path.abspath(os.path.expanduser(input))
        with open(path, "r") as file:
            return file.readlines()
    elif isinstance(input, str):
        return re.split(f"{os.linesep}|\\\\n", input)
    else:
        raise ArgumentTypeError(f"{input} is invalid.")


def get_args():
    """
    Return CLI arguments.
    """
    parser = ArgumentParser(description=f"More or less a pager")
    parser.add_argument("input", type=chkinput, help="file or string")
    return parser.parse_args()


def event_loop(stdscr, lines):  # pylint: disable=too-many-branches
    """
    Draw screen and wait for input.
    """
    page = Keys(stdscr, lines)
    cansi = Cansi(page.pad)
    footer = "Press [?] to view keybindings"
    while True:
        page.draw_footer(footer)
        for idx, line in enumerate(lines):
            cansi.addstr(idx, 0, line)

        page.refresh()

        key = stdscr.getch()
        out = page.action(key)
        if out == "quit":
            break

        if out:
            footer = out


def pager(lines):
    curses.wrapper(event_loop, lines)


def main():
    args = get_args()
    pager(args.input)


if __name__ == "__main__":
    main()
