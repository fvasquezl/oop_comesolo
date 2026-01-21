from random import choice, shuffle
from collections import deque


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
        self.rules = self.find_rules()

    def generate_all_sub_triangle_rules(self)->list:
        all_rules_list = []

        # i: Renglón de inicio (P0)
        for i in range(1, self.max_rows + 1):
            # 1. Calcular el valor del primer elemento en el renglón 'i' (T_{i-1})
            start_of_row = (i - 1) * i // 2

            # j: Columna de inicio (P0)
            for j in range(i):
                # 2. Definir los 6 puntos del sub-triángulo
                P0 = start_of_row + j
                P1 = P0 + i
                P2 = P1 + 1
                P3 = P1 + i + 1  # (P1 + i + 1)
                P4 = P2 + i + 1  # (P2 + i + 1)
                P5 = P4 + 1

                # 3. Generar las 6 reglas de salto (3 de ida, 3 de vuelta)
                lines = [
                    (P0, P1, P3), (P3, P1, P0),  # Vertical
                    (P0, P2, P5), (P5, P2, P0),  # Diagonal Derecha
                    (P3, P4, P5), (P5, P4, P3)  # Horizontal/Base
                ]

                all_rules_list.extend(lines)

        return all_rules_list

    def find_rules(self)->dict:
        all_rules_list = self.generate_all_sub_triangle_rules()
        all_rules_dict = {}

        # 1. Recolección y Eliminación de Duplicados
        for origin, delete, destination in all_rules_list:
            movement = [delete, destination]

            if origin not in all_rules_dict:
                all_rules_dict[origin] = []

            if movement not in all_rules_dict[origin]:
                all_rules_dict[origin].append(movement)

        # 2. Ordenamiento Final
        for origin in all_rules_dict:
            all_rules_dict[origin].sort()

        return dict(sorted(all_rules_dict.items()))


class Comesolo:
    def __init__(self, rows:int):
        self.board = Board(rows)
        self.rules_processor = Rules(rows)
        self.rules = self.rules_processor.rules
        self.create_board()


    def create_board(self):
        while True:
            try:
                init_pos = int(input(f"Posicion a eliminar[1-{len(self.board.cells)}]:"))
                if not( 1 <= init_pos <= len(self.board.cells)):
                    raise IndexError
                self.board.cells[init_pos -1] = "0"
                break
            except ValueError:
                print("Entrada invalida. Por favor ingrese numeros validos.")
            except IndexError:
                print(f"Solo valores entre 1 y {len(self.board.cells)} son permitidos.")
            except Exception as e:  # Catch any other unexpected errors
                print(f"Un error inesperado se ha generado: {e}")
                print("Intente de nuevo.")

        self.board.print_cells()

    def count_pegs(self) -> int:
        """Cuenta cuántas fichas quedan en el tablero."""
        return self.board.cells.count("1")

    def execute_move(self, origin: int, delete: int, destination: int):
        """Ejecuta un movimiento en el tablero."""
        cells = self.board.cells
        cells[origin] = "0"
        cells[delete] = "0"
        cells[destination] = "1"

    def undo_move(self, origin: int, delete: int, destination: int):
        """Deshace un movimiento (para backtracking)."""
        cells = self.board.cells
        cells[origin] = "1"       # Restaurar ficha en origen
        cells[delete] = "1"       # Restaurar ficha eliminada
        cells[destination] = "0"  # Vaciar destino

    def solve(self) -> list:
        """
        Resuelve el juego usando backtracking.
        Retorna la lista de movimientos si hay solución, None si no.
        """
        solution = []
        if self._backtrack(solution):
            return solution
        return None

    def _backtrack(self, solution: list) -> bool:
        """
        Algoritmo recursivo de backtracking.
        - solution: lista donde se guardan los movimientos exitosos
        """
        # Caso base: ¡Victoria! Solo queda 1 ficha
        if self.count_pegs() == 1:
            return True

        # Obtener todos los movimientos posibles
        valid_moves = self.get_valid_moves()

        # Si no hay movimientos, es un callejón sin salida
        if not valid_moves:
            return False

        # Aleatorizar el orden para obtener soluciones diferentes cada vez
        shuffle(valid_moves)

        # Probar cada movimiento
        for origin, delete, destination in valid_moves:
            # 1. Ejecutar el movimiento
            self.execute_move(origin, delete, destination)

            # 2. Guardar en la solución (optimista)
            solution.append((origin, delete, destination))

            # 3. Intentar resolver recursivamente
            if self._backtrack(solution):
                return True  # ¡Encontramos solución!

            # 4. No funcionó → BACKTRACK (deshacer)
            solution.pop()  # Quitar de la solución
            self.undo_move(origin, delete, destination)  # Restaurar tablero

        # Ningún movimiento llevó a solución
        return False

    # ========== MÉTODOS BITMASK + BFS ==========

    def board_to_bitmask(self) -> int:
        """
        Convierte el tablero actual a un entero (bitmask).
        Cada bit representa una celda: 1=ficha, 0=vacío.
        """
        bitmask = 0
        for i, cell in enumerate(self.board.cells):
            if cell == "1":
                bitmask |= (1 << i)  # Enciende el bit en posición i
        return bitmask

    def bitmask_to_board(self, bitmask: int):
        """Restaura el tablero desde un bitmask."""
        for i in range(len(self.board.cells)):
            if bitmask & (1 << i):  # Si el bit i está encendido
                self.board.cells[i] = "1"
            else:
                self.board.cells[i] = "0"

    def count_pegs_bitmask(self, bitmask: int) -> int:
        """Cuenta fichas en un bitmask (cuenta bits encendidos)."""
        return bin(bitmask).count('1')

    def get_valid_moves_bitmask(self, bitmask: int) -> list:
        """
        Obtiene movimientos válidos para un estado bitmask.
        Retorna: [(nuevo_bitmask, origen, eliminar, destino), ...]
        """
        valid_moves = []
        for origin, rules in self.rules.items():
            # Verificar si hay ficha en origen
            if bitmask & (1 << origin):
                for delete, destination in rules:
                    # Verificar: ficha en delete Y vacío en destination
                    has_delete = bitmask & (1 << delete)
                    has_dest = bitmask & (1 << destination)

                    if has_delete and not has_dest:
                        # Calcular nuevo estado
                        new_bitmask = bitmask
                        new_bitmask &= ~(1 << origin)      # Quitar de origen
                        new_bitmask &= ~(1 << delete)      # Quitar eliminada
                        new_bitmask |= (1 << destination)  # Poner en destino
                        valid_moves.append((new_bitmask, origin, delete, destination))

        return valid_moves

    def solve_bfs(self) -> list:
        """
        Resuelve usando BFS + Memoización.
        Encuentra TODAS las rutas y retorna una aleatoria.
        """
        initial_state = self.board_to_bitmask()

        # Cola: (estado_actual, camino_de_movimientos)
        queue = deque([(initial_state, [])])

        # Estados visitados para no repetir
        visited = {initial_state}

        # Guardar todas las soluciones encontradas
        all_solutions = []

        while queue:
            current_state, path = queue.popleft()

            # ¿Victoria? Solo queda 1 ficha
            if self.count_pegs_bitmask(current_state) == 1:
                all_solutions.append(path)
                continue  # Seguir buscando más soluciones

            # Explorar todos los movimientos posibles
            for new_state, origin, delete, dest in self.get_valid_moves_bitmask(current_state):
                if new_state not in visited:
                    visited.add(new_state)
                    new_path = path + [(origin, delete, dest)]
                    queue.append((new_state, new_path))

        if all_solutions:
            print(f"Se encontraron {len(all_solutions)} soluciones distintas.")
            return choice(all_solutions)  # Retorna una aleatoria

        return None

    # ========== FIN MÉTODOS BITMASK + BFS ==========

    def play_solution(self, solution: list):
        """Reproduce la solución paso a paso."""
        print("\n=== SOLUCIÓN ENCONTRADA ===\n")
        print("Estado inicial:")
        self.board.print_cells()
        print()

        for i, (origin, delete, destination) in enumerate(solution, 1):
            self.execute_move(origin, delete, destination)
            print(f"Paso {i}: {origin} → {destination} (elimina {delete})")
            self.board.print_cells()
            print()

    def get_valid_moves(self) -> list:
        """Retorna lista de movimientos válidos: [(origen, eliminar, destino), ...]"""
        cells = self.board.cells
        valid_moves = []
        for origin, rules in self.rules.items():
            if cells[origin] == "1":
                for delete, destination in rules:
                    if cells[delete] == "1" and cells[destination] == "0":
                        valid_moves.append((origin, delete, destination))
        return valid_moves

    @property
    def make_move(self):
        valid_moves = self.get_valid_moves()

        if not valid_moves:
            print(f"No hay movimientos posibles.")
            return False

        origin, delete, destination = choice(valid_moves)

        # Ejecutar el movimiento
        self.execute_move(origin, delete, destination)

        print(f"Movimiento realizado: {origin} -> {destination} (Elimina {delete})")
        self.board.print_cells()
        return True




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    comesolo = Comesolo(5)

    # Guardar posición inicial para restaurar después de resolver
    init_pos = comesolo.board.cells.index("0")

    # Elegir algoritmo
    print("\nSeleccione algoritmo:")
    print("1. Backtracking (encuentra una solución aleatoria)")
    print("2. BFS + Memoización (encuentra TODAS y elige una)")
    opcion = input("Opción [1/2]: ").strip()

    if opcion == "2":
        print("\nBuscando TODAS las soluciones con BFS...")
        solution = comesolo.solve_bfs()
    else:
        print("\nBuscando solución con Backtracking...")
        solution = comesolo.solve()

    if solution:
        # Restaurar tablero al estado inicial
        comesolo.board.initialize_cells()
        comesolo.board.cells[init_pos] = "0"

        # Mostrar la solución
        comesolo.play_solution(solution)
        print(f"¡Completado en {len(solution)} movimientos!")
    else:
        print("No existe solución óptima para esta posición inicial.")


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

