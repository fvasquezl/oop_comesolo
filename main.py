

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


class Rules:
    def __init__(self, rows:int):
        self.rows = rows
        self.rules:dict[int, list[list[int]]] = {}
        self.find_child()

    def find_left_child(self,pos, row):
        middle = pos + row + 1
        end = middle + row + 2
        self.rules.setdefault(pos,[]).append([middle,end])

    def find_right_child(self,pos, row):
        middle = pos + row + 2
        end = middle + row + 3
        self.rules.setdefault(pos,[]).append([middle,end])

    def find_child(self):
        start_pos = 0
        for row in range(self.rows):
            end_pos = start_pos + row + 1
            array_range = range(start_pos, end_pos)
            for pos in array_range:
                self.find_left_child(pos, row)
                self.find_right_child(pos,row)
                # if row >=2:
                #     self.find_brother(pos,row)
            start_pos = end_pos

        print(self.rules)
class Comesolo:
    def __init__(self, rows:int):
        self.board=Board(rows)
        self.create_board()
        self.rules=Rules(rows)

    def create_board(self):
        print("\n--- Estado inicial del tablero ---")
        self.board.print_cells()

    def create_rules(self):
        self.rules.find_child()


    def make_move(self):
        self.board.cells[1] = '0'
        print(f"\n--- Movimiento en 1 ---")
        self.board.print_cells()






# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    comesolo = Comesolo(5)
    #comesolo.make_move()



