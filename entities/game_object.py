class GameObject:
    def __init__(self, position, body_color):
        self.position = position
        self.body_color = body_color

    def get_position(self):
        return self.position

    def draw(self):
        pass
