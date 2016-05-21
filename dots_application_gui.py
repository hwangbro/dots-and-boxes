#GUI implementation of the game. Run this file to start application.


import tkinter as tk
import dots_logic
import dots_option_select
import point
import dot


_DEFAULT_FONT = ('Verdana', 16)

class BoardGUI:
    '''GUI for the game board itself'''
    
    def __init__(self, window: tk.Tk, board: dots_logic.Board) -> None:
        self._window = window
        self._board = board
        self._canvas = tk.Canvas(
            master = self._window,
            height = 400,
            width = 400,
            background = '#C4F3FF')
        
        self._canvas.grid(row = 1, column = 0,
                          sticky = tk.N + tk.W + tk.S + tk.E)

        self._window.rowconfigure(1, weight = 1)
        self._window.columnconfigure(0, weight = 1)

        
        self._rows = self._board.rows()
        self._cols = self._board.cols()


    def _draw_dots(self) -> None:
        '''Draws all the dots on the board'''
        
        self._dots = []
        self._width = self._canvas.winfo_width()
        self._height = self._canvas.winfo_height()

        for i in range(self._rows + 1):
            self._dots.append([])
            for j in range(self._cols + 1):
                Dot = dot.DotGUI(i,j)
                self._dots[i].append(Dot)
                Dot.draw(self._canvas,
                         dot.create_dot_points(i, j, self._rows, self._cols))


    def _draw_outlines(self) -> None:
        '''Draws all the outlines on the board'''
        
        width, height = self._canvas.winfo_width(), self._canvas.winfo_height()

        avg = width + height / 2
        thickness = avg * .005
        radius = 0.015 #make sure this matches the radius in dot.py in create_dot_points

        for row in range(self._rows + 1):
            x_start = self._dots[0][0].tl().frac()[0]
            x_end = self._dots[0][self._cols].br().frac()[0]
            
            top_y = self._dots[row][0].tl().frac()[1]
            bot_y = self._dots[row][0].br().frac()[1]

            x_start, x_end = x_start * width, x_end * width
            top_y, bot_y = top_y * height, bot_y * height
            
            self._canvas.create_line(x_start, top_y, x_end, top_y, width = thickness)
            self._canvas.create_line(x_start, bot_y, x_end, bot_y, width = thickness)
            
        for col in range(self._cols + 1):
            y_start = self._dots[0][0].tl().frac()[1]
            y_end = self._dots[self._rows][0].br().frac()[1]

            right_x = self._dots[0][col].tl().frac()[0]
            left_x = self._dots[0][col].br().frac()[0]

            y_start, y_end = y_start * height, y_end * height
            right_x, left_x = right_x * width, left_x * width

            self._canvas.create_line(right_x, y_start, right_x, y_end, width = thickness)
            self._canvas.create_line(left_x, y_start, left_x, y_end, width = thickness)
        

    def _draw_connections(self) -> None:
        '''Draws all the moves made on the board'''
        
        for row in self._board.boxes():
            for box in row:
                dots = box.return_connected_dots()
                for pair in dots:
                    dot_0 = self._dots[pair[0].row()][pair[0].col()]
                    dot_1 = self._dots[pair[1].row()][pair[1].col()]
                    
                    dot.connect_dots(self._canvas, dot_0, dot_1)


    def _draw_filled_boxes(self) -> None:
        '''Fills in the boxes, if completed'''

        self._width = self._canvas.winfo_width()
        self._height = self._canvas.winfo_height()

        for row in range(self._board.rows()):
            for col in range(self._board.cols()):
                box = self._board.boxes()[row][col]
                if box.completed():
                    points = (self._dots[row][col].center(), self._dots[row+1][col+1].center())
                    point_pixels = []
                    
                    for point in points:
                        point_pixels.append(point.pixel(self._width, self._height))

                    self._canvas.create_rectangle(point_pixels[0][0],
                                            point_pixels[0][1],
                                            point_pixels[1][0],
                                            point_pixels[1][1],
                                            fill = dot.translate_color(box.color()))


    def _draw_board(self) -> None:
        '''Draws the entire board'''
        
        self._canvas.delete(tk.ALL)
        self._draw_filled_boxes()
        self._draw_dots()
        self._draw_outlines()
        self._draw_connections()



class DotsApplication:
    '''Will start the entire application. Starts with option screen, then creates board'''
    
    def __init__(self, board: dots_logic.Board) -> None:
        self._board = board
        self._root_window = tk.Tk()
        self._root_window.minsize(500,500)

        self._button_down = False

        self._turn = tk.StringVar()
        self._turn.set('')

        self._orange_score = tk.StringVar()
        self._orange_score.set('Orange: 0')

        self._yellow_score = tk.StringVar()
        self._yellow_score.set('Yellow: 0')

        label_frame = tk.Frame(
            master = self._root_window)
        label_frame.grid(row = 0, column = 0, padx = 10, pady = 10,
                         sticky = tk.N + tk.S + tk.E + tk.W)

        turn_label = tk.Label(
            master = label_frame,
            textvariable = self._turn,
            font = _DEFAULT_FONT)
        turn_label.grid(row = 0, column = 1, padx = 10, sticky = tk.N)

        orange_score_label = tk.Label(
            master = label_frame,
            textvariable = self._orange_score,
            font = _DEFAULT_FONT)
        orange_score_label.grid(row = 0, column = 0, padx = 10, sticky= tk.W + tk.N)

        yellow_score_label = tk.Label(
            master = label_frame,
            textvariable = self._yellow_score,
            font = _DEFAULT_FONT)
        yellow_score_label.grid(row = 0, column = 2, padx = 10, sticky = tk.E + tk.N)

        label_frame.columnconfigure(0, weight = 1)
        label_frame.columnconfigure(1, weight = 1)
        label_frame.columnconfigure(2, weight = 1)

        self.update_score()
        self.update_turn()
        
        self._boardGUI = BoardGUI(self._root_window, self._board)
        self._boardGUI._canvas.bind('<Configure>', self._on_canvas_resized)
        self._boardGUI._canvas.bind('<Button-1>', self._on_line_clicked)
    

    def _on_canvas_resized(self, event: tk.Event) -> None:
        '''Re-draws the board when the window is resized'''

        self._boardGUI._draw_board()
        

    def _on_line_clicked(self, event: tk.Event) -> None:
        '''Determines whether or not a move has been made through clicks on the GUI'''
        
        click_point = point.from_pixel(event.x, event.y,
                                       self._boardGUI._canvas.winfo_width(),
                                       self._boardGUI._canvas.winfo_height())

        for row in range(len(self._board.boxes())):
            for col in range(len(self._board.boxes()[row])):
                pairs = self._board.boxes()[row][col].return_possible_pairs()
                for pair in pairs:
                    dot_0 = pair[0]
                    dot_1 = pair[1]
                    if dot.contains_point(click_point,
                                          self._boardGUI._dots[dot_0.row()][dot_0.col()],
                                          self._boardGUI._dots[dot_1.row()][dot_1.col()]):
                        self._board.make_move(dot_0.row(),
                                              dot_0.col(),
                                              dot_1.row(),
                                              dot_1.col())
                        self._boardGUI._draw_board()

                        self.update_score()
                        self.update_turn()
                        return
        

    def start(self) -> None:
        '''Gives tkinter control over the application'''
        
        self._root_window.mainloop()


    def update_score(self) -> None:
        '''Updates the score label'''
        
        self._orange_score.set('Orange: {}'.format(self._board.get_score()[0]))
        self._yellow_score.set('Yellow: {}'.format(self._board.get_score()[1]))
        

    def update_turn(self) -> None:
        '''Updates the turn label'''
        
        turn = dots_option_select.convert_color_to_str(self._board.turn())
        if self._board.is_game_over():
            self._turn.set('Winner: {}'.format(self._board.find_winner()))
        else:
            self._turn.set('Turn: {}'.format(turn))
            

def create_board() -> dots_logic.Board:
    '''Creates the option menu and uses the inputs to create a dots board'''
    menu = dots_option_select.OptionMenu()
    inputs = menu.answers()
    if len(inputs) != 0:
        board = dots_logic.Board(inputs[0], inputs[1])
        board.set_turn(inputs[2])
        board.set_rules(inputs[3])
        return board
    else:
        raise InputError


def run_dots() -> None:
    '''Creates and runs an instance of Dots and Boxes'''

    try:
        game_board = create_board()
        app = DotsApplication(game_board)
        app.start()
    except:
        pass




if __name__ == '__main__':
    run_dots()
