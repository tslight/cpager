#!/usr/bin/env python
"""
Simple ncurses pad scrolling example.

Example usages: cpager.py -l {1..100}
                cpager.py -f ~/path/to/file
                cpager.py -s "some super long string with\n newlines..."

Use k/j/h/l to go up/down/left/right
f/b to go to next/previous pages
g/G to go to beginning/end
q to quit
"""

import cgitb
import curses
import curses.ascii
import re
import os

from argparse import ArgumentParser, ArgumentTypeError
from cansi import Cansi
from .keys import Keys

os.environ.setdefault("ESCDELAY", "12")  # otherwise it takes an age!

# better debugging
cgitb.enable(format="text")


def chkfile(path):
    """
    Check if file exists, otherwise raise argparse exception.
    """
    if os.path.isfile(os.path.expanduser(path)):
        return os.path.abspath(os.path.expanduser(path))

    raise ArgumentTypeError(f"{path} does not exist.")


def get_args():
    """
    Return CLI arguments.
    """
    parser = ArgumentParser(description=f"Curses Pager Experiments")
    parser.add_argument("-f", "--file", type=chkfile, help="file to page")
    parser.add_argument("-l", "--list", nargs="+", help="list to page")
    parser.add_argument("-s", "--string", help=f"long string to page")
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
        # draw lines
        for idx, line in enumerate(lines):
            cansi.addstr(idx, 0, line)
            # if idx in page.matches:
            #     page.pad.chgat(idx, 0, curses.color_pair(100) | curses.A_BOLD)

        page.refresh()

        # react to input
        key = stdscr.getch()
        out = page.action(key)
        if out == "quit":
            break

        if out:
            footer = out


def parse_newlines(lines):
    for l in lines:
        if any(c in l for c in [os.linesep, "\n", "\\n"]):
            idx = lines.index(l)
            new_elements = re.split(f"{os.linesep}|\\\\n", l)
            lines.remove(l)
            for e in new_elements:
                lines.insert(idx, e)
                idx += 1

    return lines


def pager(lines):
    curses.wrapper(event_loop, lines)


def main():
    args = get_args()

    if args.file:
        path = os.path.abspath(os.path.expanduser(args.file))
        with open(path, "r") as file:
            lines = file.readlines()
    elif args.list:
        lines = parse_newlines(args.list)
    elif args.string:
        lines = re.split(f"{os.linesep}|\\\\n", lines)

    pager(lines)


if __name__ == "__main__":
    main()
