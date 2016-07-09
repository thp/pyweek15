from app import App

def main(argv):
    try:
        argv.remove('-f')
        fullscreen = True
    except ValueError:
        fullscreen = False

    entry = 'Start'
    if len(argv) == 1:
        entry = argv[0]

    App('One Whale Trip', 800, 480, fullscreen, entry).run()
