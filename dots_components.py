#Logical classes for dots and boxes

class Dot:
    '''Dot object for the logic'''
    
    def __init__(self, row: int, col: int) -> None:
        self._row = row
        self._col = col
        self._connections = []
        

    def row(self) -> None:
        '''Returns what row the dot is in'''
        return self._row


    def col(self) -> None:
        '''Returns what column the dot is in'''
        return self._col


    def connections(self) -> [(int)]:
        '''Returns the coordinates of dots that the current dot is connected to'''
        return self._connections



def make_connection(dot_1: Dot, dot_2: Dot) -> None:
    '''Makes a connection between two dots'''
    if not is_connected(dot_1, dot_2):
        dot_1._connections.append((dot_2.row(), dot_2.col()))
        dot_2._connections.append((dot_1.row(), dot_1.col()))


def translate_direction(direction: str) -> [int]:
    '''Translates a direction from string into cardinal coordinates'''
    translation = []
    if direction == 'N':
        translation = [1,0]
    elif direction == 'S':
        translation = [-1,0]
    elif direction == 'E':
        translation = [0,1]
    elif direction == 'W':
        translation = [0,-1]
    return translation


def is_connected(dot_1: Dot, dot_2: Dot) -> bool:
    '''Checks whether or not two dots are connected'''
    coords_1 = dot_1.row(), dot_1.col()
    return coords_1 in dot_2.connections()



#order of dots = tl, tr, bl, br
class Box:
    '''Box object for the logic'''
    
    def __init__(self, dots: [Dot]):
        self._dots = dots
        self._sides = [] #n s e w
        self._row = None
        self._col = None

        self.determine_location()
        self._completed = False
        self._color = 0
        

    def check_sides(self):
        '''Checks what sides of the box are completed'''
        
        sides = []
        if is_connected(self._dots[0], self._dots[1]):
            sides.append('N')
        if is_connected(self._dots[0], self._dots[2]):
            sides.append('W')
        if is_connected(self._dots[1], self._dots[3]):
            sides.append('E')
        if is_connected(self._dots[2], self._dots[3]):
            sides.append('S')
        
        self._sides = set(sides)
        

    def determine_location(self) -> None:
        '''Determines the row and column of the box'''
        
        rows = []
        cols = []
        for dot in self._dots:
            rows.append(dot.row())
            cols.append(dot.col())

        self._row = min(rows)
        self._col = min(cols)
        

    def contains_dot(self, row, col) -> bool:
        '''Returns whether or not a given dot coordinate is inside the box'''
        
        contains = False
        
        for dots in self._dots:
            if dots.row() == row and dots.col() == col:
                contains = True

        return contains
    

    def return_dot(self, row, col) -> Dot:
        '''Returns the dot of the given coordinate'''
        
        for dot in self._dots:
            if dot.row() == row and dot.col() == col:
                return dot
            

    def return_possible_pairs(self) -> [ (Dot, Dot) ]:
        '''Returns a list of the possible dot connection pairs'''
        
        pairs = []
        pairs.append((self._dots[0], self._dots[1]))
        pairs.append((self._dots[0], self._dots[2]))
        pairs.append((self._dots[1], self._dots[3]))
        pairs.append((self._dots[2], self._dots[3]))
        return pairs
    

    def return_connected_dots(self) -> [ (Dot, Dot) ]:
        '''Returns a list of pairs of dots that are connnected'''
        
        connected_dots = []
        self.check_sides()
        if 'N' in self._sides:
            connected_dots.append((self._dots[0], self._dots[1]))
        if 'W' in self._sides:
            connected_dots.append((self._dots[0], self._dots[2]))
        if 'E' in self._sides:
            connected_dots.append((self._dots[1], self._dots[3]))
        if 'S' in self._sides:
            connected_dots.append((self._dots[2], self._dots[3]))

        return connected_dots
        

    def check_completed(self) -> None:
        '''Checks if a box is completed'''
        self._completed = (len(self._sides) == 4)
        

    def set_color(self, color: int) -> None:
        '''Sets the color of a box'''
        self._color = color
        

    def completed(self) -> bool:
        '''Returns whether or not a box is completed'''
        return self._completed
    

    def row(self) -> int:
        '''Returns the row the box is in'''
        return self._row
    

    def col(self) -> int:
        '''Returns the column the box is in'''
        return self._col
    

    def dots(self) -> int:
        '''Returns the set of dots the box is made up of'''
        return self._dots
    

    def sides(self) -> [str]:
        '''Returns a list of the completed sides'''
        return self._sides
    

    def color(self) -> int:
        '''Returns the color of the box'''
        return self._color
    

    def update(self) -> None:
        '''Checks and updates the current completion status'''
        self.check_sides()
        self.check_completed()