# CURSES PAGER

## INSTALLATION

`pip install cpager`

## USAGE

Simple ncurses pad scrolling example.

``` text
Example usages: cpager.py -l {1..100}
                cpager.py -f ~/path/to/file
                cpager.py -s "some super long string with\n newlines..."
```

Use k/j/h/l or arrow keys to go up/down/left/right
f/b or PGUP/PGDN to go to next/previous pages
g/G or HOME/END to go to beginning/end
q to quit
