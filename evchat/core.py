import curses
import datetime
import json
import os
import sys
import evchat.ui

#==============================================================================
# Message class
#==============================================================================

class Message:
    def __init__(self, time=None, name=None, text=None):
        self.time = time
        self.name = name
        self.text = text

#==============================================================================
# Config class holds and manages basic app config
#==============================================================================

class Config:
    DEFAULT_FILE = os.path.expanduser("~/.evchatrc")

    def __init__(self):
        self.name = None
        self.show_timestamps = False

    def save(self, file = None):
        "Save the config to the given file. If none specified, use the default."
        # Construct the data hash
        data = { }
        data['name'] = self.name
        data['show_timestamps'] = self.show_timestamps
        # Store it to a file
        if file == None:
            file = Config.DEFAULT_FILE
        with open(file, 'w') as f:
            f.write(json.dumps(data, indent=2) + "\n")
        self

    def load(self, file = None):
        """
        Load the config from the given file. If none specified, use the default.
        Returns True on success, False on failure.
        """
        try:
            if file == None:
                file = Config.DEFAULT_FILE
            with open(file) as f:
                data = json.load(f)
                self.name = data['name']
                self.show_timestamps = data['show_timestamps']
                return True
        except:
            pass
        return False

    def has_required_data(self):
        "Return a boolean indicating if all required fields are populated."
        if self.name == None:
            return False
        return True

    def prompt_user(self):
        "Prompt the user for any missing data, and store it"
        print "Your evchat config is missing some data. Please enter:"
        self.name = raw_input("Your name: ")
        while True:
            a = raw_input("Show timestamps? (Y/n): ").lower()
            if a == '' or a == 'y' or a == 'yes':
                self.show_timestamps = True
                break
            if a == 'n' or a == 'no':
                self.show_timestamps = False
                break

#==============================================================================
# The ChatApp class is contains all lower-level UI classes, plus the main
# runtime loop.
#==============================================================================

class ChatApp:
    running = False

    def __init__(self, config, args):
        self.config = config
        self.layout = evchat.ui.Layout()
        self.args   = args
        self.screen = None

    def _start_curses(self):
        "Start curses, and initialize the `screen` class variable"
        if ChatApp.running:
            raise StandardError("Curses is already running")
        self.screen = curses.initscr()
        curses.cbreak()
        self.screen.keypad(1)
        ChatApp.running = True

    def _stop_curses(self):
        "Stop curses, and deinitialize the `screen` class variable"
        if not ChatApp.running:
            raise StandardError("Curses is not running")
        curses.nocbreak()
        self.screen.keypad(0)
        self.screen = None
        curses.endwin()
        ChatApp.running = False

    def redraw(self):
        self.screen.refresh()
        self.history.redraw()
        self.title.redraw()
        self.prompt.redraw()

    def start(self):
        "Initialize curses, draw the UI, and start the main loop"
        debug = None
        input = ''

        try:
            # Start curses and initialize all curses-based objects
            self._start_curses()
            self.title   = evchat.ui.Title(self.layout, self.screen)
            self.history = evchat.ui.History(self.layout, self.screen, self.config)
            self.prompt  = evchat.ui.Prompt(self.layout, self.screen)

            # Open the debug file
            if self.args.debug:
                debug = open('evchat.debug', 'w')

            # Run the main loop
            while True:
                self.redraw()

                # Get input
                #text = self.prompt.getstr()
                c = self.prompt.getchar()

                if debug:
                    debug.write("char: " + str(c) + "\n")
                    debug.write("KEY_UP = " + str(curses.KEY_UP) + "\n")
                    debug.write(str(c == curses.KEY_UP) + "\n")
                    debug.flush()

                text = '' #TODO

                # Parse the input
                if text == '':
                    continue
                if text == '/quit':
                    break

                # Construct and store a Message object
                now = datetime.datetime.now()
                msg = evchat.core.Message(now, self.config.name, text)
                self.history.append(msg)

                # Update the UI
                self.history.redraw()
                self.prompt.reset()

        except:
            if debug:
                msg = "Exception: " + str(sys.exc_info()[0]) + "\n"
                debug.write(msg)

        finally:
            if debug:
                debug.close

    def stop(self):
        "Stop curses and stop the app. You must call this before exiting."
        self._stop_curses()
