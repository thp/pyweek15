class Scene(object):
    def __init__(self, app):
        self.app = app
        self.next_state = None  # holds None or a string with classname of the place to go

    def process(self):
        if self.next_state:
            return self.next_state

    def resume(self, arg):
        """Called form App when being switched to"""
        self.next_state = None

    def process_input(self, event):
        pass

    def draw(self, screen):
        pass
