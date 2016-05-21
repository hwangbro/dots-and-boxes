#The main logical implementation of Dots and Boxes

import dots_components

class Board:

    def __init__(self, rows: int, cols: int) -> None:
        self._turn = 0
        self._dots = []
        self._boxes = []
        self._rows = rows #in boxes
        self._cols = cols
        self.create_board()
        self._win_rules = ''

        self._completed_box_count = 0


    def create_board(self) -> None:
        '''Creates the basic board layout'''

        for row in range(self._rows+1):
            self._dots.append([])
            for col in range(self._cols+1):
                self._dots[row].append(dots_components.Dot(row, col))
     

        for row in range(self._rows):
            self._boxes.append([])
            
            for col in range(self._cols):
                dots = []
                dots.append(self._dots[row][col])
                dots.append(self._dots[row][col+1])
                dots.append(self._dots[row+1][col])
                dots.append(self._dots[row+1][col+1])
                self._boxes[row].append(dots_components.Box(dots))


    def make_move(self, row_1: int, col_1: int, row_2: int, col_2: int) -> None:
        '''Given the two coordinates, makes a move between them if valid'''
        
        same_turn = False
        if self.is_valid_move(row_1, col_1, row_2, col_2):
            count = 0
            for row in self._boxes:
                for box in row:
                    if (box.contains_dot(row_1, col_1) and box.contains_dot(row_2, col_2)):
                        dot_1 = box.return_dot(row_1, col_1)
                        dot_2 = box.return_dot(row_2, col_2)

                        if count == 0: #if move has been made, stay same turn
                            if dots_components.is_connected(dot_1, dot_2):
                                return
                        
                        dots_components.make_connection(dot_1, dot_2)
                        count += 1
                        
                        box.update()

                        if box.completed():
                            box.set_color(self._turn)
                            same_turn = True
                            
            if not(same_turn):
                self._turn *= -1
                        

    def is_valid_move(self, row_1: int, col_1: int, row_2: int, col_2: int) -> None:
        '''Checks whether or not a move is valid'''
        
        valid_directions = [ [1,0], [-1,0], [0,1], [0,-1] ]
        new_direction = [row_2 - row_1, col_2 - col_1]
        if (self.is_valid_dot(row_1, col_1) and self.is_valid_dot(row_2, col_2)):
            return new_direction in valid_directions
        return False
    
    
    def is_valid_dot(self, row: int, col: int) -> bool:
        '''Checks whether or not a dot is within the bounds of the board'''
        
        return row >= 0 and row <= self._rows and col >= 0 and col <= self._cols
    

    def is_game_over(self) -> bool:
        '''Checks whether or not the game is over'''
        
        total = self._rows * self._cols
        count = 0
        for row in self._boxes:
            for box in row:
                if box._color != 0:
                    count += 1

        return count == total
    

    def get_score(self) -> (int):
        '''Returns the scores'''
        
        score_1 = 0
        score_2 = 0

        for row in self._boxes:
            for box in row:
                if box._color == -1:
                    score_1 += 1
                if box._color == 1:
                    score_2 += 1

        return score_1, score_2
    

    def find_winner(self) -> str:
        '''Determines the winning player based on the rules given'''
        
        orange, yellow = self.get_score()
        
        if orange > yellow:
            bigger = 'Orange'
            smaller = 'Yellow'
        elif yellow > orange:
            bigger = 'Yellow'
            smaller = 'Orange'
        else:
            bigger = 'NONE'
            smaller = 'NONE'
            
        if self._win_rules == '>':
            return bigger            
        elif self._win_rules == '<':
            return smaller


    def set_turn(self, color: int) -> None:
        '''Sets the turn'''
        
        self._turn = color


    def set_rules(self, rule: str) -> None:
        '''Sets the rules'''
        
        self._win_rules = rule


    def rows(self) -> int:
        '''Returns the number of rows on the board, in boxes'''
        
        return self._rows


    def cols(self) -> int:
        '''Returns the number of columns on the board, in boxes'''
        
        return self._cols


    def boxes(self) -> [dots_components.Box]:
        '''Returns the set of logical box objects'''
        
        return self._boxes


    def turn(self) -> int:
        '''Returns the current player turn (as an integer)'''
        
        return self._turn
