from app import App

def main(argv):
    App('One Whale Trip', 800, 480, ('-f' in argv), 'Start').run()
