from itertools import groupby
from operator import ge
import time
from collections import deque
from random import choice

# 0|0
# 1|0 1
# 2|0 1 2
# 3|0 1 2 3
# 4|0 1 2 3 4


class TriangleGeometry:
    def __init__(self, rows: int = 4, subtriange_len: int = 2) -> None:
        self.rows: int = rows
        self.total_cells: int = (self.rows + 1) * (self.rows + 2) // 2
        self.subtriange_len: int = subtriange_len
        self.subtriangles_no: int = (
            (self.rows - self.subtriange_len + 1)
            * (self.rows - self.subtriange_len + 2)
            // 2
        )

    def get_subtriangles(self) -> list[tuple[int, int, int]]:
        triangles: list[tuple[int, int, int]] = []
        for pos in range(self.subtriangles_no):
            f, c = self.index_to_coord(pos)
            triangles.append(
                (
                    self.coord_to_index(f, c),
                    self.coord_to_index(f + 1, c),
                    self.coord_to_index(f + 2, c),
                )
            )
            triangles.append(
                (
                    self.coord_to_index(f, c),
                    self.coord_to_index(f + 1, c + 1),
                    self.coord_to_index(f + 2, c + 2),
                )
            )
            triangles.append(
                (
                    self.coord_to_index(f + 2, c),
                    self.coord_to_index(f + 2, c + 1),
                    self.coord_to_index(f + 2, c + 2),
                )
            )

        return triangles

    def index_to_coord(self, pos: int) -> tuple[int, int]:
        """Dado un índice plano (0, 1, 2...), regresa (fila, columna)."""
        row = 0
        while (row + 1) * (row + 2) // 2 <= pos:
            row += 1
        col = pos - row * (row + 1) // 2
        return (row, col)

    def coord_to_index(self, i: int, j: int) -> int:
        """Dado (fila, columna), regresa el índice plano correspondiente."""

        return j + i * (i + 1) // 2


class BoardN:
    def __init__(self, geometry: TriangleGeometry) -> None:
        self.geometry: TriangleGeometry = geometry
        self.coords: dict[tuple[int, int], str] = {}
        self.pegs: int = (1 << self.geometry.total_cells) - 1

    def fill_board(self):
        pos = 0
        for i in range(self.geometry.rows + 1):
            for j in range(i + 1):
                bit_on = self.pegs & (1 << pos)
                self.coords[(i, j)] = "1" if bit_on else "0"
                pos += 1

    def print_board(self):
        self.fill_board()
        for row, group in groupby(self.coords.items(), key=lambda item: item[0][0]):
            row_str = [
                f"\033[33m{value}\033[0m" if value == "0" else value
                for (_, _), value in group
            ]
            print("  " * (self.geometry.rows - row) + "   ".join(row_str))

    def play(self):
        self.print_board()

        while True:
            try:
                init_pos = int(
                    input(f"Posicion a eliminar[1-{self.geometry.total_cells}]:")
                )
                if not (1 <= init_pos <= self.geometry.total_cells):
                    raise IndexError
                self.pegs = self.pegs & ~(1 << init_pos - 1)
                break
            except ValueError:
                print("Entrada invalida. Por favor ingrese numeros validos.")
            except IndexError:
                print(
                    f"Solo valores entre 1 y {self.geometry.total_cells} son permitidos."
                )

        self.print_board()


class RulesN:
    def __init__(self, geometry: TriangleGeometry) -> None:
        self.geometry: TriangleGeometry = geometry
        self.triangles: list[tuple[int, int, int]] = geometry.get_subtriangles()
        self.all_rules: list[tuple[int, int, int]] = []

    def generate_rules(self):
        for triangle in self.triangles:
            origen, medio, destino = triangle
            self.all_rules.append(triangle)
            self.all_rules.append((destino, medio, origen))

        for i in self.all_rules:
            print(f"{i}")


"""
class Board:
    def __init__(self, rows: int):
        self.rows: int = rows
        self.cells: list[str] = []
        self.cells_length: int = self.rows * (self.rows + 1) // 2
        self.initialize_cells()

    def initialize_cells(self, default_value: str = "1"):
        self.cells = [default_value] * self.cells_length

    def print_cells(self):
        start_pos = 0
        for i in range(self.rows):
            end_pos = start_pos + i + 1
            values = self.cells[start_pos:end_pos]
            row_str = [
                f"\033[33m{value}\033[0m" if value == "0" else value for value in values
            ]
            print("  " * (self.rows - i) + "   ".join(row_str))
            start_pos = end_pos

    def apply_move(self, origin: int, delete: int, destination: int):
        self.cells[origin] = "0"
        self.cells[delete] = "0"
        self.cells[destination] = "1"


class Rules:
    def __init__(self, rows: int):
        self.total_rows: int = rows
        self.triangle_depth: int = 3
        self.max_rows: int = self.total_rows - self.triangle_depth + 1
        self.rules = self.find_rules()

    def generate_all_sub_triangle_rules(self) -> list:
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
                    (P0, P1, P3),
                    (P3, P1, P0),  # Vertical
                    (P0, P2, P5),
                    (P5, P2, P0),  # Diagonal Derecha
                    (P3, P4, P5),
                    (P5, P4, P3),  # Horizontal/Base
                ]

                all_rules_list.extend(lines)

        return all_rules_list

    def find_rules(self) -> dict:
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


class BFSSolver:
    #Resuelve usando BFS + Bitmask. Encuentra TODAS las soluciones.

    def __init__(self, board: Board, rules: dict):
        self.board = board
        self.rules = rules

    def solve(self) -> list:
        initial_state = self._board_to_bitmask()
        queue = deque([(initial_state, [])])
        visited = {initial_state}
        all_solutions = []

        while queue:
            current_state, path = queue.popleft()

            if self._count_pegs_bitmask(current_state) == 1:
                all_solutions.append(path)
                continue

            for new_state, origin, delete, dest in self._get_valid_moves_bitmask(
                current_state
            ):
                if new_state not in visited:
                    visited.add(new_state)
                    queue.append((new_state, path + [(origin, delete, dest)]))

        return all_solutions if all_solutions else None

    def _board_to_bitmask(self) -> int:
        #Convierte el tablero a bitmask.
        bitmask = 0
        for i, cell in enumerate(self.board.cells):
            if cell == "1":
                bitmask |= 1 << i
        return bitmask

    def _count_pegs_bitmask(self, bitmask: int) -> int:
        #Cuenta bits encendidos.
        return bin(bitmask).count("1")

    def _get_valid_moves_bitmask(self, bitmask: int) -> list:
        #Obtiene movimientos válidos para un estado bitmask.
        valid_moves = []
        for origin, rules in self.rules.items():
            if bitmask & (1 << origin):
                for delete, destination in rules:
                    has_delete = bitmask & (1 << delete)
                    has_dest = bitmask & (1 << destination)

                    if has_delete and not has_dest:
                        new_bitmask = bitmask
                        new_bitmask &= ~(1 << origin)
                        new_bitmask &= ~(1 << delete)
                        new_bitmask |= 1 << destination
                        valid_moves.append((new_bitmask, origin, delete, destination))
        return valid_moves


class Comesolo:
    def __init__(self, rows: int):
        self.board = Board(rows)
        self.rules = Rules(rows).rules
        self.create_board()

    def create_board(self):
        max_pos = self.board.cells_length
        while True:
            try:
                init_pos = int(input(f"Posicion a eliminar[1-{max_pos}]:"))
                if not (1 <= init_pos <= max_pos):
                    raise IndexError
                self.board.cells[init_pos - 1] = "0"
                break
            except ValueError:
                print("Entrada invalida. Por favor ingrese numeros validos.")
            except IndexError:
                print(f"Solo valores entre 1 y {max_pos} son permitidos.")
            except Exception as e:  # Catch any other unexpected errors
                print(f"Un error inesperado se ha generado: {e}")
                print("Intente de nuevo.")

        self.board.print_cells()

    def solve(self):
        #Encuentra todas las soluciones óptimas y ejecuta una aleatoriamente
        print("\nBuscando todas las soluciones óptimas...")
        solver = BFSSolver(self.board, self.rules)
        solutions = solver.solve()

        if solutions is None:
            print("No se encontró solución para esta configuración.")
            return False

        print(
            f"Se encontraron {len(solutions)} soluciones óptimas de {len(solutions[0])} movimientos."
        )
        solution = choice(solutions)
        print("Ejecutando una solución aleatoria...\n")
        time.sleep(0.5)

        for origin, delete, destination in solution:
            self.board.apply_move(origin, delete, destination)
            print(f"Movimiento: {origin} -> {destination} (Elimina {delete})")
            self.board.print_cells()
            time.sleep(0.5)

        pegs_left = self.board.cells.count("1")
        print(f"\n¡Puzzle resuelto! Fichas restantes: {pegs_left}")
        return True

"""
if __name__ == "__main__":
    # comesolo = Comesolo(5)
    # comesolo.solve()
    rows = 4
    t = TriangleGeometry(rows=rows)
    b = BoardN(geometry=t)

    r = RulesN(geometry=t)
    print(r.generate_rules())
