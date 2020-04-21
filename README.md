# CURSES PAGER

More or less a simple Curses Python paging library...

## INSTALLATION

`pip install cpager`

## USAGE

``` text
usage: cpager [-h] [-f FILE] [-l [LIST ...]] [-s STRING]

Curses Pager Experiments

optional arguments:
  -h, --help            show this help message and exit
  -f, --file FILE       file to page
  -l, --list [LIST ...] list to page
  -s, --string STRING   long string to page
```

## KEYBINDINGS

``` text
[h][LEFT]     : Scroll left one character.
[l][RIGHT]    : Scroll right one column.
[k][UP]       : Scroll up one line.
[j][DOWN]     : Scroll down one line.
[f][PGDN]     : Scroll down a page of lines.
[b][PGUP]     : Scroll up a page of lines.
[g][HOME]     : Go to first page.
[G][END]      : Go to last page.
[/]           : Search via wildcards or regex.
[n]           : Jump to next search result.
[p]           : Jump to previous search result.
[r]           : Reset search results.
[?][F1]       : View this help page.
[w][CTRL-s]   : Save contents to file.
[q][ESC]      : Quit and exit.
```
