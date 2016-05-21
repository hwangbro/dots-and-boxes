#Methods and classes related to the GUI

import tkinter as tk
import point
import dots_components
import dots_logic

_yellow = '#FDFF5F'
_orange = '#FF943C'

class DotGUI:
    '''GUI class for a single dot'''

    def __init__(self, row: int, col: int) -> None:
        self._tl, self._br = None, None
        self._row = row
        self._col = col
        

    def row(self) -> int:
        '''Returns the row the dot is in'''
        
        return self._row
    

    def col(self) -> int:
        '''Returns the column the dot is in'''
        
        return self._col
    

    def tl(self) -> point.Point:
        '''Returns the top left bounding box point for the dot'''
        
        return self._tl
    

    def br(self) -> point.Point:
        '''Returns the bottom right bounding box point for the dot'''
        
        return self._br

    
    def draw(self, canvas: tk.Canvas, points: [point.Point]) -> None:
        '''Draws a dot onto a canvas, given its points'''
        
        self._tl, self._br = points
        self._tl_x, self._tl_y = self._tl.frac()
        self._br_x, self._br_y = self._br.frac()

        width = canvas.winfo_width()
        height = canvas.winfo_height()
        point_pixels = []
        for point in points:
            point_pixels.append(point.pixel(width, height))

        canvas.create_rectangle(point_pixels[0][0],
                           point_pixels[0][1],
                           point_pixels[1][0],
                           point_pixels[1][1],
                           fill = 'black')
        

    def center(self) -> point.Point:
        '''Returns the center point of the dot'''
        
        return point.from_frac( (self._tl_x + self._br_x)/2, (self._tl_y + self._br_y)/2 )



def create_dot_points(row: int, col: int, total_row: int, total_col: int) -> (point.Point):
    '''Given a dot's position in a board, returns bounding box points for the dot'''
    
    x = (.8 / total_col)
    y = (.8 / total_row)
    pad = 0.1
    radius = 0.015

    return (point.from_frac( (pad + (x*col) - radius), (pad + (y*row) - radius)),
           point.from_frac( (pad + (x*col) + radius), (pad + (y*row) + radius)))


def connect_dots(canvas, dot_1: DotGUI, dot_2: DotGUI):
    '''Given a canvas and two dots, draws a line between the two dots'''
    
    width, height = canvas.winfo_width(), canvas.winfo_height()
    dot_1, dot_2 = orient_dots((dot_1, dot_2))

    tl = dot_1.tl().pixel(width, height)
    br = dot_2.br().pixel(width, height)
    canvas.create_rectangle(tl[0], tl[1], br[0], br[1], fill = 'black')


def translate_color(color: int) -> str:
    if color == -1:
        return _orange
    elif color == 1:
        return _yellow
    else:
        return '#FFFFFF'


def contains_point(point, dot_1: DotGUI, dot_2: DotGUI): #doesn't check valid move
    '''Checks whether a given point is located between two dots'''
    
    dot1, dot2 = orient_dots((dot_1, dot_2))
    
    if dot_1._br_x >= dot_2._br_x and dot_1._br_y >= dot_2._br_y:
        dot1 = dot_2
        dot2 = dot_1

    point_x, point_y = point.frac()
    return (point_x > dot1._tl_x and point_x < dot2._br_x) and (
        point_y > dot1._tl_y and point_y < dot2._br_y)


def orient_dots(dots: (DotGUI)) -> (DotGUI):
    '''Correctly orients the two dots in order from top left to bottom right'''
    
    dot_1, dot_2 = dots
    if dot_1._br_x >= dot_2._br_x and dot_1._br_y >= dot_2._br_y:
        return (dot_2, dot_1)

    return (dot_1, dot_2)
