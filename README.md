# Comesolo (Peg Solitaire)

Implementación en Python del juego "Comesolo" (Peg Solitaire) usando programación orientada a objetos y múltiples algoritmos de solución.

## Descripción

El Comesolo es un juego de mesa para un jugador. El objetivo es eliminar fichas saltando sobre ellas hasta que solo quede una ficha en el tablero.

```
        0
      1   2
    3   4   5
  6   7   8   9
10  11  12  13  14
```

## Ejecución

```bash
python main.py
```

El programa solicitará:
1. Posición inicial a eliminar (1-15)
2. Algoritmo a usar (Backtracking o BFS)

## Arquitectura

El proyecto implementa el **patrón Strategy** para los algoritmos de solución:

```
┌─────────────────────────────────────────────────┐
│                   Solver (ABC)                  │
│  ───────────────────────────────────────────    │
│  + board: Board                                 │
│  + rules: dict                                  │
│  ───────────────────────────────────────────    │
│  + solve() [abstractmethod]                     │
│  + get_valid_moves()                            │
│  + count_pegs()                                 │
│  + execute_move()                               │
│  + undo_move()                                  │
└─────────────────────────────────────────────────┘
            ▲                       ▲
            │                       │
  ┌─────────┴─────────┐   ┌────────┴────────┐
  │ BacktrackingSolver│   │    BFSSolver    │
  │ ──────────────────│   │ ────────────────│
  │ + solve()         │   │ + solve()       │
  │ - _backtrack()    │   │ - _board_to_... │
  └───────────────────┘   │ - _count_pegs..│
                          │ - _get_valid... │
                          └─────────────────┘
```

### Clases principales

| Clase | Responsabilidad |
|-------|-----------------|
| `Board` | Maneja el estado del tablero triangular |
| `Rules` | Genera las reglas de salto válidas |
| `Solver` | Clase base abstracta para algoritmos |
| `BacktrackingSolver` | Implementa backtracking con orden aleatorio |
| `BFSSolver` | Implementa BFS con representación bitmask |
| `Comesolo` | Controlador principal del juego |

## Algoritmos

### 1. Backtracking

Explora recursivamente todas las posibilidades, retrocediendo cuando llega a un callejón sin salida.

```
resolver(tablero):
    si solo queda 1 ficha → Éxito
    si no hay movimientos → Backtrack

    para cada movimiento (aleatorizado):
        ejecutar movimiento
        si resolver(tablero) → retornar éxito
        deshacer movimiento  ← backtrack
```

**Características:**
- Encuentra **una** solución válida
- Orden aleatorizado para obtener soluciones diferentes cada ejecución
- Uso eficiente de memoria O(profundidad)

### 2. BFS + Bitmask

Búsqueda en anchura usando representación de bits para el estado del tablero.

**Representación Bitmask:**
```
Tablero:        Binario:              Decimal:
    1           bit 0 = 1
  1   1         bits 1,2 = 11
1   0   1  →    bits 3,4,5 = 101  →   31455
  1   1   1     bits 6-9 = 1111
1   1   1   1   bits 10-14 = 11111
```

**Operaciones de bits:**
```python
bitmask |= (1 << i)      # Encender bit (poner ficha)
bitmask &= ~(1 << i)     # Apagar bit (quitar ficha)
bitmask & (1 << i)       # Verificar bit (¿hay ficha?)
bin(bitmask).count('1')  # Contar fichas
```

**Características:**
- Encuentra **TODAS** las soluciones posibles
- Selecciona una aleatoriamente
- Memoización para evitar estados repetidos
- 15 celdas = 15 bits = estados eficientes

## Comparación de algoritmos

| Aspecto | Backtracking | BFS + Bitmask |
|---------|--------------|---------------|
| Encuentra | Una solución | Todas las soluciones |
| Memoria | O(profundidad) | O(estados únicos) |
| Velocidad | Rápido para 1 | Más lento (explora todo) |
| Aleatoriedad | Shuffle por nivel | Elige de todas |

## Agregar nuevo solver

```python
class MiNuevoSolver(Solver):
    """Descripción del algoritmo."""

    def solve(self) -> list:
        # Implementación
        # Retorna lista de movimientos [(origen, eliminar, destino), ...]
        # o None si no hay solución
        pass
```

Luego registrarlo en `Comesolo.set_solver()`:

```python
def set_solver(self, solver_type: str):
    if solver_type == "mi_solver":
        self.solver = MiNuevoSolver(self.board, self.rules)
    # ...
```

## Estructura del proyecto

```
oop_comesolo/
├── main.py        # Código principal
├── README.md      # Este archivo
└── CLAUDE.md      # Guía para Claude Code
```

## Reglas del juego

1. Se inicia con 14 fichas y 1 espacio vacío
2. Una ficha puede saltar sobre otra adyacente hacia un espacio vacío
3. La ficha saltada se elimina
4. El objetivo es quedar con exactamente 1 ficha

### Movimientos válidos

Cada ficha puede saltar en 6 direcciones (si hay ficha intermedia y destino vacío):
- Vertical arriba/abajo
- Diagonal izquierda arriba/abajo
- Diagonal derecha arriba/abajo
