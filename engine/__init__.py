from .app import App


def frames():
    app = App('One Whale Trip', 800, 480, 'Start')
    yield from app.run()


def main():
    for _ in frames():
        ...
