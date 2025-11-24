

class Board:
    def __init__(self, rows:int):
        self.rows = rows
        self.cells:list[str]= []
        self.cells_length = self.rows * (self.rows +1) // 2
        self.initialize_cells()

    def initialize_cells(self, default_value:str="1"):
        self.cells = [default_value] * self.cells_length

    def print_cells(self):
        start_pos = 0
        for i in range(self.rows):
            end_pos = start_pos + i + 1
            values = self.cells[start_pos:end_pos]
            row_str = [f"\033[33m{value}\033[0m" if value == "0" else value for value in values]
            print("  " * (self.rows - i) + "   ".join(row_str))
            start_pos = end_pos

class Comesolo:
    def __init__(self, rows:int):
        self.board =Board(rows)
        self.create_board()

    def create_board(self):
        print("\n--- Estado inicial del tablero ---")
        self.board.print_cells()


    def make_move(self):
        self.board.cells[1] = '0'
        print(f"\n--- Movimiento en 1 ---")
        self.board.print_cells()



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    comesolo = Comesolo(5)
    comesolo.make_move()


