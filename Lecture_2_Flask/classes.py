# defining a new class of things named Point
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# calling the class Point I just created
p = Point(3, 5)
print(p.x)
print(p.y)