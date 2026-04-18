"""
- Our very last challenge (maybe).

++ Add the @property decorator into the package Shape, 
++ so all the protected data could be accessed this way.
    
++ Add @classmethod decorator to Shape, in order to change 
++ define and change the type of shape of each class.
    
++ Add a custom decorator in Shape co show the computation 
++ time of at least one operation. e.g: compute_area.
"""

import math
import time

#$ time decorator extracted from class notes 
def timing_decorator(func):
  def inner(*args, **kwargs):
    start_time = time.time()
    # ejecucion de la funcion que recibe como argumento
    result = func(*args, **kwargs)
    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.4f} seconds")
    return result
  # retorna la funcion decorada sin ejecutarla
  return inner


#* Define point as base class
class Point:
    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y

    def compute_distance(self, point: "Point") -> float:
        return ((self.x - point.x)**2 + (self.y - point.y)**2)**0.5

    def __repr__(self):
        return f"(x: {self.x}, y: {self.y})"

class Numerical:
    error_diff = 1e-8
    p0 = Point(0.0,0.0)

#- define Line class
class Line(Numerical):
    def __init__(self, start: Point, end: Point):
        if start.compute_distance(end) < self.error_diff:
            start = self.p0
            end = Point(1,1)
        self.start = start
        self.end = end
        self.length = self.compute_length()


    #- use the Point instance param to calculate length 
    def compute_length(self) -> float:
        return self.start.compute_distance(self.end)

    #- compute dot product to assist in angle computation
    @timing_decorator
    def dot(self, l0: Line):
        dx = (self.end.x - self.start.x)*(l0.end.x - l0.start.x)
        dy = (self.end.y - self.start.y)*(l0.end.y - l0.start.y)
        return dx + dy

    def __repr__(self):
        return f"x in [{self.start.x}, {self.end.x}] and y in [{self.start.y}, {self.end.y}]"

type Vertices = list[Point]
type Edges    = list[Line]
type Vector   = list[float]

#? @property is the pythonic way to create getters
#? @property.setter is the pythonic way to create setters
class Shape:
    def __init__(self, vertices=None, edges=None, angles=None, is_regular=False):
        self._vertices = vertices if vertices else []
        self._edges = edges if edges else []
        self._angles = angles if angles else []
        self._is_regular = is_regular

    @classmethod
    def from_vertices(cls, vertices: Vertices):
        """
        Factory method to 'define' a shape based on vertex count.
        This changes which 'type' of shape is being initialized.
        """
        if len(vertices) == 3:
            return Triangle(vertices=vertices)
        elif len(vertices) == 4:
            #? by default every figure is a rectangle so, well
            return Rectangle(vertices=vertices)
        else:
            return cls(vertices=vertices)

    # --- Vertices ---
    @property
    def vertices(self) -> Vertices:
        return self._vertices

    @vertices.setter
    def vertices(self, value: Vertices):
        self._vertices = value

    # --- Edges ---
    @property
    def edges(self) -> Edges:
        return self._edges

    @edges.setter
    def edges(self, value: Edges):
        self._edges = value

    # --- Angles ---
    @property
    def angles(self) -> Vector:
        return self._angles

    # --- Is Regular ---
    @property
    def is_regular(self) -> bool:
        return self._is_regular

    @is_regular.setter
    def is_regular(self, value: bool):
        self._is_regular = value

    # @ overridden methods
    def compute_area(self):
        pass

    def compute_perimeter(self):
        pass

    def compute_inner_angles(self):
        pass
    
"""
class Triangle
% it is necessary to create the edges in a closed-ordered loop
% a-b-c or c-b-a
"""
class Triangle(Shape):
    def __init__(self, vertices=None, edges=None, angles=None, is_regular=False):
        super().__init__(vertices, edges, angles, is_regular)

    #- Re-linking the getter to allow the setter override
    @Shape.vertices.getter
    def vertices(self):
        return self._vertices
    
    @vertices.setter
    def vertices(self, value: Vertices):
        """
        input must be 3-length vector so i add
        those validations in order to garantee this 
        condition
        """
        if len(value) > 3:
            raise ValueError("There is more vertices than expected...")
        elif len(value) < 3:
            raise ValueError("Few arguments than expected...")
        else:
            self._vertices = value
    
    #- Re-linking the getter to allow the setter override
    @Shape.edges.getter
    def edges(self):
        return self._edges
    
    @edges.setter
    def edges(self, value: Edges):
        """
        input must be 3-length vector so i add
        those validations in order to garantee this 
        condition
        """
        if len(value) > 3:
            raise ValueError("There is more edges than expected...")
        elif len(value) < 3:
            raise ValueError("Few arguments than expected...")
        else:
            self._edges = value
    
    @Shape.angles.getter
    def angles(self):
        return self._angles
    
    @angles.setter
    def angles(self, value):
        """
        input must be 3-length vector so i add
        those validations in order to garantee this 
        condition
        """
        if len(value) > 3:
            raise ValueError("There is more angles than expected...")
        elif len(value) < 3:
            raise ValueError("Few arguments than expected...")
        else:
            self._angles = value

    #@overriding methods

    def compute_perimeter(self):
        """
        if 3 edges are not set then 
        it is a potential error 'cause it is
        mandatory to sum 3 edges to get perimeter
        """
        if len(self.edges) != 3:
            raise IndexError("There are no 3 edges")
        return sum([s.compute_length() for s in self._edges])

    def compute_area(self):
        """
        if 3 edges are not set then 
        it is a potential error 'cause it is
        mandatory to use 3 edges to compute area
        """
        if len(self.edges) != 3:
            raise IndexError("There are no 3 edges")
        a, b, c = [s.compute_length() for s in self._edges]
        if ((a + b > c) and (a + c > b) and (b + c > a)):
            #++ perimeter
            p = a + b + c
            #++ semiperimeter
            s = p / 2
            #++ Area using Heron's formula 
            #% area = sqrt(s * (s-a) * (s-b) * (s-c))
            return (s * (s - a) * (s - b) * (s - c))**(0.5)
        else: 
            raise ValueError("Triangle is not valid. Fix it before to calc area...")
            return None
    
    def compute_inner_angles(self):
        """
        if 3 edges are not set then 
        it is a potential error 'cause it is
        not possible to calculate angles without 
        edges
        """
        if len(self.edges) != 3:
            raise IndexError("There are no 3 edges")

        #++ using dot product definition
        #% a.b = ||a||.||b||.cos(x)
        a, b, c = self.edges
        la, lb, lc = [s.compute_length() for s in self._edges]

        ab = a.dot(b)
        bc = b.dot(c)
        ca = c.dot(a)

        cos_ab = ab/(la*lb)
        cos_bc = bc/(lb*lc)
        cos_ca = ca/(lc*la)

        self.angles = [
            round(math.degrees(math.acos(cos_ab)),2), 
            round(math.degrees(math.acos(cos_bc)),2), 
            round(math.degrees(math.acos(cos_ca)),2)
        ]

class Isosceles(Triangle):
    def __init__(self):
        super().__init__([],[],[], False)

#? this is the only one that is regular
class Equilateral(Triangle):
    def __init__(self):
        super().__init__([],[],[], True)

class Scalene(Triangle):
    def __init__(self):
        super().__init__([],[],[], False)

#? is this necessary?
class TriRectangle(Triangle):
    def __init__(self):
        super().__init__([],[],[], False)

class Rectangle(Shape):
    def __init__(self, vertices=None, edges=None, angles=None, is_regular=False):
        super().__init__(vertices, edges, angles, is_regular)
    
    #- Re-linking the getter to allow the setter override
    @Shape.vertices.getter
    def vertices(self):
        return self._vertices

    @vertices.setter
    def vertices(self, value: Vertices):
        """
        input must be 4-length vector so i add
        those validations in order to garantee this 
        condition
        """
        if len(value) > 4:
            raise ValueError("There is more vertices than expected...")
        elif len(value) < 4:
            raise ValueError("Few arguments than expected...")
        else:
            self._vertices = value
    
    #- Re-linking the getter to allow the setter override
    @Shape.edges.getter
    def edges(self):
        return self._edges

    @edges.setter
    def edges(self, value: Edges):
        """
        input must be 4-length vector so i add
        those validations in order to garantee this 
        condition
        """
        if len(value) > 4:
            raise ValueError("There is more edges than expected...")
        elif len(value) < 4:
            raise ValueError("Few arguments than expected...")
        else:
            self._edges = value
    
    @Shape.angles.getter
    def angles(self):
        return self._angles
    
    @angles.setter
    def angles(self, value):
        """
        input must be 4-length vector so i add
        those validations in order to garantee this 
        condition
        """
        if len(value) > 4:
            raise ValueError("There is more angles than expected...")
        elif len(value) < 4:
            raise ValueError("Few arguments than expected...")
        else:
            self._angles = [90.0, 90.0, 90.0, 90.0]
    #@overriding methods

    def compute_perimeter(self):
        """
        if 4 edges are not set then 
        it is a potential error 'cause it is
        mandatory to sum 4 edges to get perimeter
        """
        if len(self.edges) != 4:
            raise IndexError("There are no 4 edges")
        return sum([s.compute_length() for s in self._edges])

    def compute_area(self):
        """
        if 4 edges are not set then 
        it is a potential error 'cause it is
        mandatory 2 edges to compute area but 
        the shape needs 4 to technically exists
        """
        if len(self.edges) != 4:
            raise IndexError("There are no 4 edges")

        lengths = [s.compute_length() for s in self._edges]
        return max(lengths) * min(lengths)
    
    def compute_inner_angles(self):
        """
        if 4 edges are not set then 
        it is a potential error 'cause it is
        not possible to calculate angles without 
        edges
        """
        if len(self.edges) != 4:
            raise IndexError("There are no 4 edges")

        self.angles = [90.0, 90.0, 90.0, 90.0]


class Square(Rectangle):
    def __init__(self, vertices=None, edges=None):
        # A Square is always regular and has 90 degree angles
        super().__init__(vertices, edges, [90.0]*4, True)

    def compute_area(self):
        """
        if 4 edges are not set then 
        it is a potential error 'cause it is
        mandatory 2 edges to compute area but 
        the shape needs 4 to technically exists
        """
        if len(self.edges) != 4:
            raise IndexError("There are no 4 edges")
        # Polymorphism: Optimization for Square
        side = self._edges[0].compute_length()
        return side ** 2

# --- Verification Script ---
# -- AI Assisted
def run_tests():
    print("--- 1. Testing @classmethod Factory ---")
    # Define 3 points for a triangle
    p1, p2, p3 = Point(0, 0), Point(4, 0), Point(0, 3)
    
    # Create shape via the classmethod
    triangle_shape = Shape.from_vertices([p1, p2, p3])
    print(f"Object Type: {type(triangle_shape).__name__}")
    
    print("\n--- 2. Testing @property Setters/Getters ---")
    # Verify we can access vertices via property
    print(f"Vertices before update: {triangle_shape.vertices}")
    
    # Verify validation in Triangle property setter
    try:
        triangle_shape.vertices = [p1, p2] # Should fail
    except ValueError as e:
        print(f"Validation Caught: {e}")

    print("\n--- 3. Testing Custom Timing Decorator ---")
    # We need to manually add edges to compute angles/dot products
    l1 = Line(p1, p2)
    l2 = Line(p2, p3)
    l3 = Line(p3, p1)
    triangle_shape.edges = [l1, l2, l3]
    
    # This will trigger the @timing_decorator inside dot()
    print("Calculating inner angles (triggers dot product timing):")
    triangle_shape.compute_inner_angles()
    print(f"Calculated Angles: {triangle_shape.angles}")

    print("\n--- 4. Testing Specific Shape Logic (Rectangle) ---")
    p4 = Point(4, 3)
    rect_shape = Shape.from_vertices([p1, p2, p4, p3])
    print(f"Object Type: {type(rect_shape).__name__}")
    
    # Verify specific area logic
    rect_shape.edges = [Line(p1, p2), Line(p2, p4), Line(p4, p3), Line(p3, p1)]
    print(f"Rectangle Area: {rect_shape.compute_area()}")

if __name__ == "__main__":
    run_tests()
