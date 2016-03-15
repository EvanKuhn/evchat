#!/usr/bin/env python
import curses
import os

CHAT_APP_VERSION = "0.0.1"
CHAT_APP_TITLE = "evchat v" + CHAT_APP_VERSION

#==============================================================================
# Simple class to calculate the layout of our UI and windows.
#==============================================================================

class Layout:
    def __init__(self):
        "Determine the terminal size, and size of each window"

        # Get terminal size
        self.rows, self.cols = Layout.terminal_size()

        # Calculate dimensions of each window
        self.title_rows         = 1
        self.title_cols         = self.cols
        self.title_start_row    = 0
        self.title_start_col    = 0

        self.history_rows       = self.rows - 2
        self.history_cols       = self.cols
        self.history_start_row  = 1
        self.history_start_col  = 0

        self.prompt_rows        = 1
        self.prompt_cols        = self.cols
        self.prompt_start_row   = self.rows - 1
        self.prompt_start_col   = 0

    @staticmethod
    def terminal_size():
        "Return the current terminal size, as a tuple of (rows, cols)"
        rows, cols = os.popen('stty size', 'r').read().split()
        return (int(rows), int(cols))

#==============================================================================
# This just displays the title
#==============================================================================

class Title:
    def __init__(self, layout, screen):
        self.window = curses.newwin(layout.title_rows, layout.title_cols,
            layout.title_start_row, layout.title_start_col)
        start_col = (layout.title_cols - len(CHAT_APP_TITLE)) / 2
        self.window.addstr(0, start_col, CHAT_APP_TITLE)

    def redraw(self):
        self.window.refresh()

#==============================================================================
# The History class displays the chat history.
#==============================================================================

class History:
    def __init__(self, layout, screen):
        self.lines = []
        self.layout = layout
        self.screen = screen
        self.window = curses.newwin(layout.history_rows, layout.history_cols,
            layout.history_start_row, layout.history_start_col)
        # Because we have a border, the number of visible rows/cols is fewer
        self.visible_rows = self.layout.history_rows - 2
        self.visible_cols = self.layout.history_cols - 2

    def append(self, str):
        "Append a line of text to the history. Does not redraw."
        self.lines.append(str)

    def redraw(self):
        self.window.clear()
        self.window.border(0)

        # Add the last N lines, where N is the number of visible rows
        row = 1
        for line in self.lines[-self.visible_rows:]:
            self.window.addstr(row, 1, line)
            row += 1

        self.window.refresh()

#==============================================================================
# The Prompt class prompts the user for text.
#==============================================================================

class Prompt:
    def __init__(self, layout, screen):
        self.layout = layout
        self.screen = screen
        self.window = curses.newwin(layout.prompt_rows, layout.prompt_cols,
            layout.prompt_start_row, layout.prompt_start_col)
        self.window.addstr('> ')

    def get(self):
        "Get input from the user. Returns a string."
        return self.window.getstr()

    def redraw(self):
        "Redraw the prompt window"
        self.window.refresh()

    def reset(self):
        "Reset the prompt to '> ' and redraw"
        self.window.clear()
        self.window.addstr('> ')
        self.redraw()

#==============================================================================
# The ChatApp class is contains all lower-level UI classes, plus the main
# runtime loop.
#==============================================================================

class ChatApp:
    # Curses screen object
    screen = None

    def __init__(self):
        # Start curses. Will raise if we try to start curses more than once.
        self.start_curses()
        self.layout  = Layout()
        self.screen  = ChatApp.screen
        self.title   = Title(self.layout, self.screen)
        self.history = History(self.layout, self.screen)
        self.prompt  = Prompt(self.layout, self.screen)

    def start_curses(self):
        "Start curses, and initialize the `screen` class variable"
        if ChatApp.screen != None:
            raise StandardError("Curses screen has already been initialized")
        ChatApp.screen = curses.initscr()

    def stop_curses(self):
        "Stop curses, and deinitialize the `screen` class variable"
        if ChatApp.screen == None:
            raise StandardError("Curses screen has not been initialized")
        curses.endwin()
        ChatApp.screen = None

    def redraw(self):
        self.screen.refresh()
        self.history.redraw()
        self.title.redraw()
        self.prompt.redraw()

    def run(self):
        "Where the magic happens"
        while True:
            self.redraw()
            str = self.prompt.get()
            if str == '':
                continue
            if str == '/quit':
                break
            self.history.append(str)
            self.history.redraw()
            self.prompt.reset()

#==============================================================================
# Main
#==============================================================================


app = ChatApp()
app.run()
app.stop_curses()
