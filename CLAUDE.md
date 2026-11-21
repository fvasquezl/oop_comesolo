# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Comesolo is a Python implementation of triangular Peg Solitaire (also known as "Cracker Barrel puzzle"). The game uses a triangular board where pieces can jump over adjacent pieces to remove them, with the goal of leaving as few pieces as possible.

This project also doubles as an OOP study exercise: `main.py` is mid-refactor, moving from a flat-index representation to a coordinate/bitmask-based one, as a way to practice composition, dependency injection, and Python typing.

## Running the Application

```bash
python main.py
```

`main.py` currently runs the **new, in-progress implementation** (see Architecture below): it builds a `TriangleGeometry` and a `BoardN`, then `Game(board).run()` prints the full board, asks for a 1-indexed position to remove, and prints the board again. Nothing else happens yet (no moves, no solver). The original game loop (`Comesolo(5).solve()`) lives inside the legacy `"""..."""` block and is not wired to `__main__`.

There are no runtime dependencies (stdlib only) and no test suite. A local venv at `.venv` (git-ignored, created with `python3 -m venv .venv`) holds `basedpyright` for type checking: `.venv/bin/basedpyright main.py` (currently 0 errors). To check behavior, run `main.py` or import the classes from a `python -c` / REPL session.

## Architecture

`main.py` currently contains two implementations side by side.

### Legacy implementation (kept as reference, wrapped in a `"""..."""` block)

Three classes plus a solver:

- **Board**: manages the triangular board state as a flat list. Cells are indexed 0-14 for a 5-row triangle, where "1" = peg present, "0" = empty hole. `print_cells()` renders the board with ANSI coloring.
- **Rules**: generates all valid jump rules for the triangle. Uses a sub-triangle approach where each 3-row sub-triangle defines 6 possible jumps (3 directions × 2 ways). Rules are stored as `{origin: [[delete, destination], ...]}`.
- **BFSSolver**: BFS + bitmask solver for a given `Board`/`Rules` pair. The goal test is exactly **1 peg left**, and it returns `None` if no such end state is reachable. Because of the global `visited` set, "all solutions" really means one shortest path per distinct single-peg end state, not every move sequence.
- **Comesolo**: main game controller. Combines `Board`, `Rules`, and `BFSSolver` — asks for the initial position to remove, then `solve()` finds all optimal solutions and plays one at random.

This block is intentionally kept, not dead code — the new implementation's formulas (e.g. sub-triangle jump generation) are being ported from it. It relies on `deque`, `choice` and `time`, which are not imported at the top of the file (a note inside the block lists them) — add those imports if the block is ever re-enabled.

### New implementation (in progress)

- **TriangleGeometry**: pure triangle geometry, independent of any board/game state. Given `rows`, computes `total_cells` and `subtriangles_no`, and converts between flat index and `(fila, columna)` coordinates via `index_to_coord`/`coord_to_index` (mutually inverse; both raise `IndexError` for out-of-triangle input). The class constant `JUMP_SPAN = 2` (a jump covers 3 cells in a line) fixes the sub-triangle size; it is not a constructor parameter, because the offsets in `get_subtriangles()` are written for that size. `get_subtriangles()` loops over every sub-triangle vertex `(f, c)` in rows `0..rows-2` and returns the flat-index triples (origin, jumped-over, destination) for its 3 sides — left, right diagonal, base.
- **BoardN**: receives a `TriangleGeometry` through its constructor (dependency injection) and owns only state + display. State is a single `int` bitmask (`self.pegs`, one bit per cell, all set initially). Methods: `has_peg(pos)`, `remove(pos)`, `apply_move(origen, medio, destino)` (no validity check — the caller must pass a legal jump), `count()` (`int.bit_count()`), and `print_board()` (groups cells by row with `itertools.groupby`, empty holes in yellow).
- **RulesN**: receives only a `TriangleGeometry` (deliberately *not* `BoardN`'s state) — rules depend solely on geometry, never on which cells currently hold a peg. On construction it builds `self.rules: dict[int, list[tuple[int, int]]]`, i.e. `{origen: [(medio, destino), ...]}`, by turning each sub-triangle side into a forward + reverse jump. No sub-triangle side is repeated, so no deduplication is needed. Unlike legacy `Rules`, the lists are not sorted. `moves_from(origen)` returns the jumps for one cell. Verified against a brute-force enumeration of all straight-line jumps for 6-, 15-, 21- and 28-cell boards.
- **Game**: user interaction. Receives a `BoardN`; `ask_initial_position()` asks for a 1-indexed position, validates it, and returns it 0-indexed; `run()` shows the board, removes that peg, and shows it again. It does not receive `RulesN` yet.

**`rows` means something different in each implementation:** legacy `Board(5)`/`Rules(5)` take the number of rows (5 → 15 cells). `TriangleGeometry(rows=4)` takes the **0-indexed last row** (4 → rows 0..4 → 15 cells, `total_cells = (rows+1)(rows+2)/2`). In the same way, `JUMP_SPAN=2` corresponds to the legacy `triangle_depth=3`. So `TriangleGeometry(rows=4)` is the same board as legacy `5`, and it yields 6 sub-triangles → 36 jump rules.

Design intent: rules/geometry stay decoupled from the board's runtime peg state (mirrors the legacy `Rules`/`Board` split), and shared calculations (like index↔coordinate conversion) live in one place (`TriangleGeometry`) instead of being duplicated across classes.

Not yet done: `Game` isn't given `RulesN`, and there's no move-execution loop or valid-move generator (legacy `BFSSolver._get_valid_moves_bitmask` is the template: combine `RulesN.moves_from` with `BoardN.has_peg`); no solver has been ported to the new bitmask representation.

## Board Indexing

The triangular board is stored/numbered as a flat list with positions:
```
        0
      1   2
    3   4   5
  6   7   8   9
10  11  12  13  14
```
Both the legacy `Board` and the new `TriangleGeometry.index_to_coord`/`coord_to_index` use this same numbering.

## Readme.md

`Readme.md` holds scratch notes in Spanish, not user docs: the hand derivation of the sub-triangle formula (`P1=P0+i`, `P2=P1+1`, `P3=P1+i+1`, `P4=P2+i+1`, `P5=P4+1`) and a list of candidate solver approaches for later (backtracking, Q-learning, DQN, MCTS, A*).

## Language

Code comments and user prompts are in Spanish.
