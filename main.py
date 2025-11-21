

class Board:
    def __init__(self, rows:int):
        self.rows = rows
        self.board:list[str]= []
        self.board_length = self.rows * (self.rows +1) // 2
        self.create_board()

    def create_board(self, default_value:str="1"):
        self.board = [default_value] * self.board_length

    def print_board(self, values: list[str], i: int) -> None:
        row_str = [f"\033[33m{value}\033[0m" if value=="0" else value for value in values]
        print("  " * (self.rows - i) + "   ".join(row_str))

    def create_row(self):
        start_pos = 0
        for i in range(self.rows):
            end_pos = start_pos + i + 1
            values = self.board[start_pos:end_pos]
            self.print_board(values, i)
            start_pos = end_pos


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    board = Board(5)
    board.create_row()
