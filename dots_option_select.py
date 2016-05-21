## How to select the game options (# of rows, # of cols, who starts)
import tkinter as tk

class OptionMenu:
    
    def __init__(self) -> None:
        self._window = tk.Tk()
        self._window.wm_title('Options Menu')
        self._window.resizable(width = False, height = False)
        
        self._answers = []

        self._create_labels()
        self._print_labels()
        self._create_option_menus()
        self._print_option_menus()
        self._create_button()

        self._window.mainloop()

        
    def _create_labels(self) -> None:
        '''Creates the labels for the option menu'''
        
        self._label_1 = tk.Label(master = self._window,
                                 text = '# of Rows',
                                 font = ('Verdana', 12))
        self._label_2 = tk.Label(master = self._window,
                                 text = '# of Cols',
                                 font = ('Verdana', 12))
        self._label_3 = tk.Label(master = self._window,
                                 text = 'Who Moves First',
                                 font = ('Verdana', 12))
        self._label_4 = tk.Label(master = self._window,
                                 text = 'Who Wins',
                                 font = ('Verdana', 12))


    def _print_labels(self) -> None:
        '''Prints the labels onto the window'''
        
        self._label_1.grid(row = 0, column = 0, padx = 20,
                           sticky = tk.N + tk.S + tk.E + tk.W)
        self._label_2.grid(row = 0, column = 1, padx = 20,
                           sticky = tk.N + tk.S + tk.E + tk.W)
        self._label_3.grid(row = 2, column = 0, padx = 20,
                           sticky = tk.N + tk.S + tk.E + tk.W)
        self._label_4.grid(row = 2, column = 1, padx = 20,
                           sticky = tk.N + tk.S + tk.E + tk.W)
        

    def _create_option_menus(self) -> None:
        '''Creates the option menu widgets'''
        
        responses_1_2 = ['3', '4', '5', '6', '7', '8', '9', '10']
        self.response_1 = tk.StringVar()
        self.response_1.set('5')
        self._option_1 = tk.OptionMenu(self._window,
                                       self.response_1,
                                       *responses_1_2)

        self.response_2 = tk.StringVar()
        self.response_2.set('5')
        self._option_2 = tk.OptionMenu(self._window,
                                       self.response_2,
                                       *responses_1_2)

        responses_3 = ['Orange', 'Yellow']
        self.response_3 = tk.StringVar()
        self.response_3.set('Orange')
        self._option_3 = tk.OptionMenu(self._window,
                                       self.response_3,
                                       *responses_3)

        responses_4 = ['Most Filled', 'Least Filled']
        self.response_4 = tk.StringVar()
        self.response_4.set('Most Filled')
        self._option_4 = tk.OptionMenu(self._window,
                                       self.response_4,
                                       *responses_4)


    def _print_option_menus(self) -> None:
        '''Prints the option menu widgets to the window'''
        
        self._option_1.grid(row = 1, column = 0, padx = 20, pady = 5,
                            sticky = tk.N + tk.S + tk.E + tk.W)
        self._option_2.grid(row = 1, column = 1, padx = 20, pady = 5,
                            sticky = tk.N + tk.S + tk.E + tk.W)
        self._option_3.grid(row = 3, column = 0, padx = 20, pady = 5,
                            sticky = tk.N + tk.S + tk.E + tk.W)
        self._option_4.grid(row = 3, column = 1, padx = 20, pady = 5,
                            sticky = tk.N + tk.S + tk.E + tk.W)
        

    def _create_button(self) -> None:
        '''Creates the start button for the option menu'''

        self._button_frame = tk.Frame(master = self._window)
                
        self._button_frame.grid(row = 0, column = 2, rowspan = 2,
                                padx = 10, pady = 10,
                                sticky = tk.N + tk.S + tk.E + tk.W)

        
        self._button_frame.rowconfigure(0, weight = 1)
        self._button_frame.rowconfigure(1, weight = 1)
        self._button_frame.rowconfigure(2, weight = 1)
        
        self._button = tk.Button(master = self._button_frame, text = 'Start!',
                                 font = ('Verdana', 16),
                                 command = self._on_button_clicked)
        self._button.grid(row = 1, column = 0)
        

    def _on_button_clicked(self) -> None:
        '''Gets the responses from the option menu and destroys the window'''
        
        self._answers = []
        self._answers.append(int(self.response_1.get()))
        self._answers.append(int(self.response_2.get()))
        self._answers.append(convert_color(self.response_3.get()))
        self._answers.append(convert_winner_rule(self.response_4.get()))

        self._window.destroy()
        

    def answers(self) -> [str]:
        return self._answers
        

def convert_color(color: str) -> int:
    '''Translates into the abbreviation for the color'''
    
    if color == 'Orange':
        return -1
    if color == 'Yellow':
        return 1
    

def convert_color_to_str(color: int) -> str:
    '''Translates the color from int to string'''
    
    if color == 1:
        return 'Yellow'
    if color == -1:
        return 'Orange'
    if color == 0:
        return 'None'
    

def convert_winner_rule(rule: str) -> str:
    '''Translates into the necessary symbol for most or least pieces'''
    
    if rule == 'Most Filled':
        return '>'
    if rule == 'Least Filled':
        return '<'
