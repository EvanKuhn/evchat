import argparse
import curses
import sys
import evchat

def run():
    "Run the evchat program"

    # Parse arguments
    parser = argparse.ArgumentParser(
        description = 'evchat is a simple chat program for your terminal',
        formatter_class = argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('-d', '--debug', dest='debug', default=False,
        action='store_true', help='print debugging output to file evchat.debug')
    parser.add_argument('--version', dest='version', default=False,
        action='store_true', help='print the version and exit')
    args = parser.parse_args()

    # Show version?
    if args.version:
        pyver = sys.version_info
        python_version = "%s.%s.%s" % (pyver.major, pyver.minor, pyver.micro)
        print "evchat version %s (using Python %s, curses %s)" % \
          (evchat.VERSION, python_version, curses.version)
        sys.exit()

    # Make sure we have all the necessary config data
    conf = evchat.core.Config()
    conf.load()
    if not conf.has_required_data():
        conf.prompt_user()
        conf.save()

    # Run the app
    app = evchat.core.ChatApp(conf, args)
    try:
        app.start()
    except KeyboardInterrupt:
        pass
    finally:
        app.stop()
