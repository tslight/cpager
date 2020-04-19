# CURSES PAGER

## INSTALLATION

`pip install cpager`

## USAGE

Simple ncurses pad scrolling example.

``` text
usage: cpager [-h] [-f FILE] [-l LIST [LIST ...]] [-s STRING]

Curses Pager Experiments

optional arguments:
  -h, --help            show this help message and exit
  -f, --file FILE       file to page
  -l, --list [LIST ...] list to page
  -s, --string STRING   long string to page
```

| **KEY**     | **ACTION**                |
|:------------|:--------------------------|
| `k`,`UP`    | Move up one line          |
| `j`,`DOWN`  | Move down one line        |
| `h`,`LEFT`  | Move left one char        |
| `l`,`RIGHT` | Move right one char       |
| `g`,`HOME`  | Jump to first line        |
| `G`,`END`   | Jump to last line         |
| `f`,`PGDN`  | Jump down a page of lines |
| `b`,`PGUP`  | Jump up a page of lines   |
