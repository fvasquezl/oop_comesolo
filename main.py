
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
        self.total_rows = rows
        self.triangle_depth = 3
        self.max_rows = self.total_rows - self.triangle_depth + 1
        self.sub_triangles = self.find_sub_triangles()


    def find_sub_triangles(self):
        all_rules_dict = {}

        for i in range(1, self.max_rows + 1):
            start_of_row = (i - 1) * i // 2


            for j in range(i):
                P0 = start_of_row + j
                P1 = P0 + i
                P2 = P1 + 1
                P3 = P1 + i+ 1
                P4 = P2 + i+ 1
                P5 = P4 + 1

                lines = [
                    # Vertical (P0 - P1 - P3)
                    (P0, P1, P3), (P3, P1, P0),
                    # Diagonal Derecha (P0 - P2 - P5)
                    (P0, P2, P5), (P5, P2, P0),
                    # Horizontal/Base (P3 - P4 - P5)
                    (P3, P4, P5), (P5, P4, P3)
                ]

                for origen, eliminar, destino in lines:

                    # El movimiento es [Pieza a Eliminar, Destino]
                    movimiento = [eliminar, destino]

                    # Si el origen ya está en el diccionario, agregar el nuevo movimiento
                    if origen in all_rules_dict:
                        # Solo agregamos el movimiento si no es un duplicado
                        if movimiento not in all_rules_dict[origen]:
                            all_rules_dict[origen].append(movimiento)
                    else:
                        # Si el origen es nuevo, creamos la entrada
                        all_rules_dict[origen] = [movimiento]


        print(all_rules_dict)
        return lines






class Comesolo:
    def __init__(self, rows:int):
        self.board=Board(rows)
        self.rules = Rules(rows)
        self.create_board()


    def create_board(self):
        print("\n--- Estado inicial del tablero ---")
        self.board.print_cells()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    comesolo = Comesolo(5)
    #comesolo.make_move()

#            0
#          1   2
#        3   4   5
#      6   7   8   9
#    10  11  12  13  14


#
#                         P0   P1     P2      P3         P4        P5
# [                          P0+i    P1+1   P1+i+1     P2+i+1     P4+1
# 0 [0, 1, 2, 3, 4, 5]  [ 0, 0+1=1, 1+1=2, 1+1+1= 3,  2+1+1= 4,  4+1= 5]
# 1 [1, 3, 4, 6, 7, 8]  [ 1, 1+2=3, 3+1=4, 3+2+1= 6,  4+2+1= 7,  7+1= 8]
# 2 [2, 4, 5, 7, 8, 9]  [ 2, 2+2=4, 4+1=5, 4+2+1= 7,  5+2+1= 8,  8+1= 9]
# 3 [3, 6, 7,10,11,12]  [ 3, 3+3=6, 6+1=7, 6+3+1=10,  7+3+1=11, 11+1=12]
# 4 [4, 7, 8,11,12,13]  [ 4, 4+3=7, 7+1=8, 7+3+1=11,  8+3+1=12, 12+1=13]
# 5 [5, 8, 9,12,13,14]  [ 5, 5+3=8, 8+1=9, 8+3+1=12,  9+2+1=13, 13+1=14]
# ]

#         P0-0
#       P1-1  P2-2      P3 = P1+i+1
#     P3-3  P4-4  P5-5    P4 = P2+i+1
#
#   [0, 1, 3], [0, 2, 5], [3, 4, 5]]


# [
# 0 [0, 1, 2, 3, 4, 5]
#  0  1   3
# [P0,P1,P3]
# [

#
#  0 {[1,3],[2,5]}
#  3 {[1,0],[4,5]}
#  5 {[2,0],[4,3]}
#

