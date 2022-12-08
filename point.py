# import statements typically go here
# write your class definition here
import math
class Point:
    '''Represents a point in 2D euclidean space'''
    def __init__(self, x=0,y=0):
        self.x = x
        self.y = y
    def polar(self):
        r = math.sqrt(self.x**2 + self.y**2)
        theta = math.atan(self.y/self.x)
        theta = math.degrees(theta)
        return f"({r}, {theta})"

    def __str__(self) -> str:
        return f"({self.x},{self.y})"
        
    def __add__(self,other):
        if isinstance(other,Point):
            x = self.x + other.x
            y = self.y + other.y
            
        else: 
            x = self.x + float(other)
            y = self.y + float(other)
        return Point(x, y)
    
    def __radd__(self, other):
        '''Python first tries to call __add__ method. If this fails, it tries
        to fix it by calling __radd__ for reverse addition of the right operand'''
        if isinstance(other,Point):
            x = self.x + other.x
            y = self.y + other.y
            
        else: 
            x = self.x + float(other)
            y = self.y + float(other)
        return Point(x, y)

    def __sub__(self,other):
        if isinstance(other, Point):
            x = self.x - other.x
            y = self.y - other.y
        else:
            x = self.x - float(other)
            y = self.y - float(other)
        return Point(x, y)

    def __rsub__(self,other):
        if isinstance(other, Point):
            x = self.x - other.x
            y = self.y - other.y
        else:
            x = self.x - float(other)
            y = self.y - float(other)
        return Point(x, y)


    def __mul__(self,n):
        x = self.x * n
        y = self.y * n
        return Point(x, y)
    
    def __rmul__(self,n):
        x = self.x * n
        y = self.y * n
        return Point(x, y)

    def __doc__():
        """point.Point = class Point(builtins.object)
            | point.Point(x=0.0, y=0.0)
            |
            | Represents a point in two-dimensional Euclidean space
            |
            | attributes:
            | x: distance along one axis
            | y: distance along the other perpendicular axis
            |
            | Methods defined here:
            |
            | __add__(self, point)
            |
            | __init__(self, x=0.0, y=0.0)
            | Initialize self. See help(type(self)) for accurate signature.
            |
            | __mul__(self, factor)
            |
            Version 1.00
            | __radd__(self, point)
            |
            | __rmul__(self, factor)
            |
            | __rsub__(self, point)
            |
            | __str__(self)
            | Return str(self).
            |
            | __sub__(self, point)
            |
            | polar(self)
            |
            | ----------------------------------------------------------------------
            | Data descriptors defined here:
            |
            | __dict__
            | dictionary for instance variables (if defined)
            |
            | __weakref__
            | list of weak references to the object (if defined)"""
        pass
    
def print_attributes(obj):
    for attr in vars(obj):
        print(attr, getattr(obj,attr))




def distance(point1,point2):
    x_dist = point1.x - point2.x
    y_dist = point1.y - point2.y
    dist = math.sqrt(x_dist**2 + y_dist**2)
    return dist




def main():
    pt1 = Point()
    pt2 = Point(1,2)
    print(pt1.x)
    print(pt1.y)
    print(pt2.x)
    print(pt2.y)

    print(pt2.polar())

    pt3 = Point(4,5)
    print(pt2 + pt3)
    print(pt2 - pt3)
    print(pt2*2)
    
    print(pt2 + 2)
    print(3 + pt2)
    print(pt2 - 2)
    print(3 - pt2)
    print(2*pt2)

    print(distance(pt1, pt2))
    print(distance(pt2, pt3))

    # help('point.Point')

    # print_attributes(pt2)
    print(vars(pt2))
    for attr in vars(pt2):
        print(attr)
        print(getattr(pt2,attr))

if __name__ == '__main__':
    main()     

