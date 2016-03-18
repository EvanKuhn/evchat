import argparse
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
        print evchat.TITLE
        sys.exit()

    # Make sure we have all the necessary config data
    conf = evchat.core.Config()
    conf.load()
    if not conf.has_required_data():
        conf.prompt_user()
        conf.save()

    # Run the app
    app = evchat.core.ChatApp(conf)
    try:
        app.start()
    except KeyboardInterrupt:
        pass
    finally:
        app.stop()
