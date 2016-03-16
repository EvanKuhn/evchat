import curses
import json
import evchat.ui

#==============================================================================
#
#==============================================================================

class Config:
    DEFAULT_FILE = "~/.evchatrc"

    def __init__(self):
        self.name = "TODO"
        pass

    def save(self, file = None):
        "Save the config to the given file. If none specified, use the default."
        if file == None:
            file = Config.DEFAULT_FILE
        print "TODO: save config to %s" % file
        self

    def load(self, file = None):
        "Load the config from the given file. If none specified, use the default."
        if file == None:
            file = Config.DEFAULT_FILE
        print "TODO: load config from %s" % file
        self

    def has_required_data(self):
        "Return a boolean indicating if all required fields are populated."
         # TODO
        True

    def prompt_user(self):
        "Prompt the user for any missing data, and store it"
        print "TODO: prompt the user for config data"
        pass

#==============================================================================
# The ChatApp class is contains all lower-level UI classes, plus the main
# runtime loop.
#==============================================================================

class ChatApp:
    # Curses screen object
    screen = None

    def __init__(self, config):
        self.config = config
        self.layout = evchat.ui.Layout()

    def _start_curses(self):
        "Start curses, and initialize the `screen` class variable"
        if ChatApp.screen != None:
            raise StandardError("Curses screen has already been initialized")
        ChatApp.screen = curses.initscr()

    def _stop_curses(self):
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

    def start(self):
        "Initialize curses, draw the UI, and start the main loop"

        # Start curses and initialize all curses-based objects
        self._start_curses()
        self.screen  = ChatApp.screen
        self.title   = evchat.ui.Title(self.layout, self.screen)
        self.history = evchat.ui.History(self.layout, self.screen)
        self.prompt  = evchat.ui.Prompt(self.layout, self.screen)

        # Run the main loop
        while True:
            self.redraw()
            str = self.prompt.get()
            if str == '':
                continue
            if str == '/quit':
                break
            str = "%s: %s" % (self.config.name, str)
            self.history.append(str)
            self.history.redraw()
            self.prompt.reset()

    def stop(self):
        "Stop curses and stop the app. You must call this before exiting."
        self._stop_curses()
