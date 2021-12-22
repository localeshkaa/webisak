class Rectangle:
     all_rectangles = []#     def __init__(self, side_a=1, side_b=1, x=0, y=0):
         self.side_a = side_a
         self.side_b = side_b
         self.x = x
         self.y = y
         self.__class__.all_rectangles.append(self)

     @staticmethod
     def rectangle_area(side_a, side_b):
         return side_a * side_b

     @classmethod
     def total_area(cls):
         total = 0
         for r in cls.all_rectangles:
             total = total + cls.rectangle_area(r.side_a, r.side_b)
         return total




 class Square(Rectangle):
     def __init__(self, side=1, x=0, y=0):
         self.side = side
         super().__init__(x, y)


 r = Rectangle(5, 8)
 s = Square(1)
 print(r.rectangle_area(r.side_a, r.side_b))
 print(s.rectangle_area(s.side, s.side))
 
